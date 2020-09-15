var fs = require("fs")
var parse = require('@loaders.gl/core').parse
var GLTFLoader = require('@loaders.gl/gltf').GLTFLoader

async function main() {
    //var data = fs.readFileSync("output/2-frame.json")
    //var data = '{"type":"xviz/state_update","data":{"update_type":"INCREMENTAL","updates":[{"timestamp":1600151747.5448382,"poses":{"/vehicle_pose":{"timestamp":1600151747.5448382,"position":[4.313834104116149,-29.68822721757169,0.0],"orientation":[0.0,0.0,533383917.4190758]}}}]}}'
    //var data = fs.readFileSync("../data/kitti-2-frame.json")
    //console.log(data)
    var data = fs.readFileSync("../data/2CylinderEngine.gltf")
    console.log(data)
    var body = await parse(data, GLTFLoader)
    console.log(body)
}

main()
