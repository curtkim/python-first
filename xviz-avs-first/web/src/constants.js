import {CarMesh} from 'streetscape.gl';

/* eslint-disable camelcase */
export const MAPBOX_TOKEN = process.env.MapboxAccessToken; // eslint-disable-line

export const MAP_STYLE = 'mapbox://styles/mapbox/light-v9';

export const XVIZ_CONFIG = {
  PLAYBACK_FRAME_RATE: 10
};

export const CAR = CarMesh.sedan({
  origin: [1.08, -0.32, 0],
  length: 4.3,
  width: 2.2,
  height: 1.5,
  color: [160, 160, 160]
});

export const APP_SETTINGS = {
  viewMode: {
    type: 'select',
    title: 'View Mode',
    data: {TOP_DOWN: 'Top Down', PERSPECTIVE: 'Perspective', DRIVER: 'Driver'}
  },
  showTooltip: {
    type: 'toggle',
    title: 'Show Tooltip'
  }
};

export const XVIZ_STYLE = {
  '/tracklets/objects': [{name: 'selected', style: {fill_color: '#ff8000aa'}}],
  '/lidar/points': [{style: {point_color_mode: 'ELEVATION'}}]
};