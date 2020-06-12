import {XVIZFileLoader} from 'streetscape.gl';

export default new XVIZFileLoader({
  timingsFilePath:
    '/output/0-frame.json',
  getFilePath: index =>
    `/output/${index +1}-frame.glb`,
  worker: true,
  maxConcurrency: 6
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