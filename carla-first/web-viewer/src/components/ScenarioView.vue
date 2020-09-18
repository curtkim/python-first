<template>
  <div class="scenario">
    <div>
      <h3>{{ msg }}</h3>
      <button v-on:click="prevFrame(20)">prev20</button>      
      <button v-on:click="prevFrame(5)">prev5</button>      
      <button v-on:click="prevFrame(1)">prev</button>
      <button v-on:click="nextFrame(1)">next</button>
      <button v-on:click="nextFrame(5)">next5</button>
      <button v-on:click="nextFrame(20)">next20</button>
      <span>{{ frame }} </span>
      <span>{{ carpose.rotation[2] }} zoom={{ viewState.zoom }} {{ viewState.rotationX }} {{ viewState.rotationOrbit }}</span>
    </div>
    <div class="sliderContainer">
      <el-slider v-model="frame" :max="128"></el-slider>
    </div>
    <div class="container">
      <div class="left">
        <img :src="imageUrls[7]"/>
        <img :src="imageUrls[0]"/>
        <img :src="imageUrls[1]"/><br/>
        <img :src="imageUrls[6]"/>
        <span class="dummy">&nbsp;</span>
        <img :src="imageUrls[2]"/><br/>
        <img :src="imageUrls[5]"/>
        <img :src="imageUrls[4]"/>
        <img :src="imageUrls[3]"/>
      </div>
      <div class="right">
        <canvas id="deckcanvas"></canvas>
      </div>
    </div>    
  </div>
</template>

<script>
const fetch = require('node-fetch');

import {Deck} from '@deck.gl/core';
import {COORDINATE_SYSTEM, OrbitView,   
  DirectionalLight,
  LightingEffect,
  AmbientLight
} from '@deck.gl/core';
import {PointCloudLayer} from '@deck.gl/layers';
import {GeoJsonLayer} from '@deck.gl/layers';
import {mat4, quat} from 'gl-matrix';

function chunking(data, length) {
  var result = [];
  for (var i = 0; i < data.length; i += length) {
    result.push(data.subarray(i, i + length));
  }
  return result;
}

function base64_farray(base64str){
  var blob	= window.atob(base64str)
  var arr = Uint8Array.from(blob, c => c.charCodeAt(0))
  var farr = new Float32Array(arr.buffer)
  return chunking(farr, 3)
}

const INITIAL_VIEW_STATE = {
  target: [0,0,0],
  rotationX: 85,
  rotationOrbit: -90,
  //orbitAxis: 'Y',
  fov: 70,
  zoom: 2
};

//const BASE_URL = '//alpha-mk.kakao.com/dn/mobdata/omega-perception/temp';
const BASE_URL = '//localhost:8000/_out';

const LIDAR_HEIGHT = 2.4
const MAX_FRAME = 128

export default {
  name: 'ScenarioView',
  props: {
    msg: String,
  },
  data() {
    return {
      frame : 1,
      mapLanes : [],
      carpose: {
        location: [0,0,0],
        rotation: [0,0,0],
      },
      carposeMatrix: mat4.create(),
      lidarPoints : [],
      viewState: {
        ...INITIAL_VIEW_STATE,
      },
    }
  },
  created() {
    this.fetchMap();
    this.fetchFrame();
  },
  beforeDestroy() {
    if (this.deck) 
      this.deck.finalize();
  },
  mounted() {
    this.deck = new Deck({
      canvas: "deckcanvas",
      views: new OrbitView({near: 0.1, far: 450}),
      initialViewState: this.viewState,
      controller: true,
      onViewStateChange: (props) => {
        const {viewState} = props;
        this.viewState = viewState;
        //console.log(viewState.target, viewState.rotationOrbit, viewState.rotationX, viewState.zoom)
        //this.$emit("viewStateChange", viewState);
      },
      layers: this.makeLayers(),
    });
  },
  methods: {
    /*
    make_resource_url(id){
      return `${BASE_URL}/${id}`;
    },
    */
    fetchMap() {
      fetch('lane.geojson')
        .then(res => res.json())
        .then(json => {
          this.mapLanes = json
        });
    },
    fetchFrame() {
      var _frame = this.frame
      fetch(`${BASE_URL}/${this.paddedFrame}_frame.json`)
        .then(res => res.json())
        .then(json => {
          if( _frame != this.frame) return;

          var loc = json.carpose.location
          var rot = json.carpose.rotation

          var q = quat.create()
          quat.fromEuler(q, 0, 0, -1*rot[2]+270)
          mat4.fromRotationTranslationScale(this.carposeMatrix, q, [loc[0], -1*loc[1], LIDAR_HEIGHT], [1, -1, -1])
          this.carpose = json.carpose

          console.log(this.viewState)
          this.viewState = Object.assign(this.viewState, {
            target: [loc[0], -1*loc[1], loc[2]],
            rotationOrbit: rot[2]-270,
          })

          this.lidarPoints = base64_farray(json.lidar)
          console.log('this.lidarPoints.length',this.lidarPoints.length)
          console.log(this.viewState.target, this.viewState.rotationOrbit, this.viewState.rotationX, this.viewState.zoom)
          
        });
    },
    update() {
      this.deck.setProps({
        layers: this.makeLayers(),
        initialViewState: this.viewState,
      });
    },    
    prevFrame(step=1) {
      var frame = this.frame - step
      this.frame = Math.max(frame, 1)
    },
    nextFrame(step=1) {
      var frame = this.frame + step
      this.frame = Math.min(frame, MAX_FRAME)
    },

    makeLayers() {
      return [
        new PointCloudLayer({
          id: 'point-cloud-layer',
          visible: true,
          data: this.lidarPoints,
          //pickable: true,
          //coordinateSystem: COORDINATE_SYSTEM.CARTESIAN,
          modelMatrix: this.carposeMatrix,
          pointSize: 2,
          opacity: 0.9,
          getPosition: d => {
            return d//[d[0],d[1],-1*d[2]]
          },
          getNormal: [0, 1, 0],
          getColor: [160, 160, 180],
          onHover: ({object, x, y}) => {
            if( object){
              const tooltip = object.join(', ');
              console.log(tooltip, x, y);
            }
          }
        }),
        new GeoJsonLayer({
          id: 'geojson-layer',
          data: this.mapLanes,
          pickable: false,
          stroked: true,
          filled: false,
          extruded: false,
          lineWidthScale: 0.2,
          lineWidthMinPixels: 1,
          getFillColor: [160, 160, 180],
          getLineColor: [100, 0, 0],
          getRadius: 1,
          getLineWidth: 1,
          getElevation: 30
        }),
      ]
    }
  },
  watch: {
    frame: function() {
      this.fetchFrame()
    },
    lidarPoints: function(){
      console.log('lidarPoints updated')
      this.update();
    },    
  },
  computed: {
    paddedFrame() {
      var TARGET_LENGTH = 5
      return (this.frame + '').padStart(TARGET_LENGTH, '0')
    },
    imageUrls() {      
      var result = []
      for (var i = 0; i < 8; i++)
        result.push(`${BASE_URL}/${this.paddedFrame}_camera${i}.png`)        
      return result;
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

.sliderContainer {
  padding: 0 20px 0 10px;
}

div.left {
  position: absolute;
  width: 50%;
}
div.left img {
  width: 33.3%;
  /* object-fit: fill; */
}
div.left span.dummy {
  display: inline-block;
  width: 33.3%;
}

div.right {
  position: absolute;
  width: 50%;
  left: 50%;
  height: 800px;
}

div.right canvas {
  border : 0px solid silver;
  background-color: #e0e0e0;
}

</style>
