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
    extensions: ['.js', '.jsx', '.css', '.mjs', '.cjs'],
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
        test: /\.(?:js|jsx|cjs|mjs)$/i,
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

function createConfiguration(folder, optionalEntry = null) {
  /** @type {import('webpack').Configuration} */
  const entry = {
    ...config,
    name: folder,
    context: path.resolve(projectRoot, 'frontend', folder, 'src', 'js'),
    entry: {},
    output: {
      path: path.resolve(projectRoot, 'frontend', folder, 'static'),
      filename: '[name].js',
      publicPath: path.resolve(projectRoot, 'static'),
    },
  };

  entry.entry[folder] = [`./${folder}.jsx`];
  if (optionalEntry) {
    entry.entry[optionalEntry] = [`./${optionalEntry}.jsx`];
  }

  return entry;
}

function getConfiguration() {
  const outputs = [createConfiguration('config'), createConfiguration('shows', 'show'), createConfiguration('movies', 'movie')];
  for (const item of outputs) {
    if (item.mode === 'production') {
      const serviceWorker = new GenerateSW();
      item.plugins = [...item.plugins, serviceWorker];
    }
  }

  return outputs;
}

// eslint-disable-next-line import/no-anonymous-default-export
export default () => getConfiguration();
