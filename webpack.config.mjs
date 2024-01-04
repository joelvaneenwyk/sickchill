//
// Generated using webpack-cli https://github.com/webpack/webpack-cli
//

import {join, dirname} from 'node:path';
import {fileURLToPath} from 'node:url';

import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import {GenerateSW} from 'workbox-webpack-plugin';

const fileUrl = fileURLToPath(import.meta.url);
const projectRoot = dirname(fileUrl);

/** @type {string} */
const stylesHandler = MiniCssExtractPlugin.loader;

/** @type {import('webpack').Configuration} */
export const config = {
  // eslint-disable-next-line n/prefer-global/process
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  resolve: {
    extensions: ['.js', '.jsx', '.css'],
  },
  devServer: {
    open: true,
    host: 'localhost',
  },
  plugins: [
    new MiniCssExtractPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.(?:js|jsx)$/i,
        loader: 'babel-loader',
      },
      {
        test: /\.css$/i,
        use: [stylesHandler, 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [stylesHandler, 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(?:eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
        type: 'asset',
      },
    ],
  },
};

/** @type {import('webpack').Configuration} */
export const configurations = {
  ...config,
  name: 'config',
  context: join(projectRoot, 'frontend', 'config', 'src', 'js'),
  entry: {
    config: ['./config.jsx'],
  },
  output: {
    path: join(projectRoot, 'frontend', 'config', 'static'),
    filename: '[name].js',
    publicPath: join(projectRoot, 'static'),
  },
};

/** @type {import('webpack').Configuration} */
export const shows = {
  ...config,
  name: 'shows',
  context: join(projectRoot, 'frontend', 'shows', 'src', 'js'),
  entry: {
    shows: ['./shows.jsx'],
    show: ['./show.jsx'],
  },
  output: {
    path: join(projectRoot, 'frontend', 'shows', 'static'),
    filename: '[name].js',
    publicPath: join(projectRoot, 'static'),
  },
};

/** @type {import('webpack').Configuration} */
export const movies = {
  ...config,
  name: 'movies',
  context: join(projectRoot, 'frontend', 'movies', 'src', 'js'),
  entry: {
    movies: ['./movies.jsx'],
    movie: ['./movie.jsx'],
  },
  output: {
    path: join(projectRoot, 'frontend', 'movies', 'static'),
    filename: '[name].js',
    publicPath: join(projectRoot, 'static'),
  },
};

export default function getConfiguration() {
  const outputs = [configurations, shows, movies];
  for (const item of outputs) {
    if (item.mode === 'production') {
      const serviceWorker = new GenerateSW();
      item.plugins = [...item.plugins, serviceWorker];
    }
  }

  return config;
}
