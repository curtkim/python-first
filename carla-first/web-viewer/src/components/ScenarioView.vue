<template>
  <div class="scenario">
    <h1>{{ msg }}</h1>
    <div class="container">
      <span class="left">
        <img :src="imageUrl"/>
      </span>
      <span class="right">
        <canvas id="deckcanvas"></canvas>
      </span>
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
import {mat4} from 'gl-matrix';

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
  target: [229, -54, 0],
  rotationX: 45,
  rotationOrbit: 0,
  //orbitAxis: 'Y',
  fov: 50,
  zoom: 3.5
};

//const BASE_URL = '//alpha-mk.kakao.com/dn/mobdata/omega-perception/temp';
const BASE_URL = '//localhost:8000/_out';


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
      height: '90%',
      width: '50%',
      views: new OrbitView({near: 0.1, far: 450}),
      initialViewState: this.viewState,
      controller: true,
      onViewStateChange: (props) => {
        const {viewState} = props;        
        this.viewState = viewState;
        console.log(viewState.target, viewState.rotationOrbit, viewState.rotationX)
        this.$emit("viewStateChange", viewState);
      },
      layers: this.computedLayers,
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
      fetch(`${BASE_URL}/pc_000001.txt`)
        .then(res => res.json())
        .then(json => {
          
          //mat4.invert(this.carposeMatrix, mat4.fromValues(...json.carposeMatrix))
          //console.log(this.carposeMatrix)
          //console.log(json.carpose)
          var t = mat4.create()
          mat4.fromTranslation(t, [229.99989318847656, -54.99998092651367, 3])
          var r = mat4.create()
          mat4.fromRotation(r, Math.PI/2, [0,0,1])
          mat4.mul(this.carposeMatrix, t, r)

          this.carpose = json.carpose
          //this.viewState.target = json.carpose.location
          //this.viewState.OrbitView
          this.lidarPoints = base64_farray(json.lidar)
        });
    },
    update() {
      this.deck.setProps({
        layers: this.computedLayers,
      });
    },    
  },
  watch: {
    lidarPoints: function(){
      this.update();
    },
  },
  computed: {
    imageUrl() {
      return `${BASE_URL}/rgb_000001.png`;
    },
    computedLayers() {
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
            return [d[0],d[1],-1*d[2]]
          },
          getNormal: [0, 1, 0],
          getColor: [255, 255, 255],
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
          getFillColor: [160, 160, 180, 200],
          getLineColor: [100, 0, 0],
          getRadius: 1,
          getLineWidth: 1,
          getElevation: 30
        }),
      ]
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}

span.left {
  width: 50%;
}
span.left img {
  background-color: silver;
  width: 50%;
  height: 100%;
}

span.right {
  width: 50%;
}

span.right canvas {
  border : 1px solid silver;
}

</style>
