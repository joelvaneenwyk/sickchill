/* eslint-disable unicorn/prefer-node-protocol */
//
// Generated using webpack-cli https://github.com/webpack/webpack-cli
//

import path from 'path';
import {fileURLToPath} from 'url';

import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import {GenerateSW} from 'workbox-webpack-plugin';

export const projectRoot = path.dirname(fileURLToPath(import.meta.url));

/** @type {import('webpack').Configuration} */
const config = {
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
        use: [MiniCssExtractPlugin.loader, 'css-loader'],
      },
      {
        test: /\.s[ac]ss$/i,
        use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
      },
      {
        test: /\.(?:eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
        type: 'asset',
      },
    ],
  },
};

/** @type {import('webpack').Configuration} */
const configurations = {
  ...config,
  name: 'config',
  context: path.resolve(projectRoot, 'frontend', 'config', 'src', 'js'),
  entry: {
    config: ['./config.jsx'],
  },
  output: {
    path: path.resolve(projectRoot, 'frontend', 'config', 'static'),
    filename: '[name].js',
    publicPath: path.resolve(projectRoot, 'static'),
  },
};

/** @type {import('webpack').Configuration} */
const shows = {
  ...config,
  name: 'shows',
  context: path.resolve(projectRoot, 'frontend', 'shows', 'src', 'js'),
  entry: {
    shows: ['./shows.jsx'],
    show: ['./show.jsx'],
  },
  output: {
    path: path.resolve(projectRoot, 'frontend', 'shows', 'static'),
    filename: '[name].js',
    publicPath: path.join(projectRoot, 'static'),
  },
};

/** @type {import('webpack').Configuration} */
const movies = {
  ...config,
  name: 'movies',
  context: path.resolve(projectRoot, 'frontend', 'movies', 'src', 'js'),
  entry: {
    movies: ['./movies.jsx'],
    movie: ['./movie.jsx'],
  },
  output: {
    path: path.resolve(projectRoot, 'frontend', 'movies', 'static'),
    filename: '[name].js',
    publicPath: path.resolve(projectRoot, 'static'),
  },
};

function getConfiguration() {
  const outputs = [configurations, shows, movies];
  for (const item of outputs) {
    if (item.mode === 'production') {
      const serviceWorker = new GenerateSW();
      item.plugins = [...item.plugins, serviceWorker];
    }
  }

  return config;
}

// eslint-disable-next-line import/no-anonymous-default-export
export default {
  ...getConfiguration(),
};
