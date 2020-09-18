import {mat4, quat} from 'gl-matrix';

describe('gl-matrix', function () {

  describe('quat', function () {
    it('test', function () {      
      var a = quat.create()
      quat.fromEuler(a, 90, 0, 0)
      console.log(a)
    })
  })

  describe('mat4', function () {
    it('test', function () {      
      var a = mat4.create() // new Float32Array(16)
      mat4.fromTranslation(a, [1,2,3])
      console.log(a)

      mat4.fromScaling(a, [-1, -1, -1])
      console.log(a)
    })
  })
})
