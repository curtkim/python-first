import {XVIZFileLoader} from 'streetscape.gl';

export default new XVIZFileLoader({
  timingsFilePath:
    'http://localhost:8000/output/0-frame.json',
  getFilePath: index =>
    `http://localhost:8000/output/${index +1}-frame.json`,
  worker: true,
  maxConcurrency: 4
});

/*
export default new XVIZFileLoader({
  timingsFilePath:
    'https://raw.githubusercontent.com/uber/xviz-data/master/kitti/2011_09_26_drive_0005_sync/0-frame.json',
  getFilePath: index =>
    `https://raw.githubusercontent.com/uber/xviz-data/master/kitti/2011_09_26_drive_0005_sync/${index +
      1}-frame.glb`,
  worker: true,
  maxConcurrency: 4
});
*/