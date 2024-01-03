//
// Generated using webpack-cli https://github.com/webpack/webpack-cli
//

import {resolve as _resolve} from 'node:path';

import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import {GenerateSW} from 'workbox-webpack-plugin';

/** @type bool */
const isProduction = process.env.NODE_ENV === 'production';

/** @type string */
const stylesHandler = MiniCssExtractPlugin.loader;

/** @type {import('webpack').Configuration} */
const config = {
  context: _resolve(_resolve(), 'frontend/templates'),
  entry: {
    shows: ['./js/shows.jsx'],
    show: ['./js/show.jsx'],
  },
  output: {
    path: _resolve() + '/frontend/static',
    filename: '[name].js',
    publicPath: _resolve('static'),
  },
  resolve: {
    extensions: ['.js', '.jsx', '.css'],
  },
  devServer: {
    open: true,
    host: 'localhost',
  },
  plugins: [
    new MiniCssExtractPlugin(),

    // Add your plugins here
    // Learn more about plugins from https://webpack.js.org/configuration/plugins/
  ],
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/i,
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
        test: /\.(eot|svg|ttf|woff|woff2|png|jpg|gif)$/i,
        type: 'asset',
      },

      // Add your rules for custom modules here
      // Learn more about loaders from https://webpack.js.org/loaders/
    ],
  },
};

export default () => {
  if (isProduction) {
    config.mode = 'production';

    config.plugins.push(new GenerateSW());
  } else {
    config.mode = 'development';
  }

  return config;
};
