/**
 *
 */

import react from '@eslint-react/eslint-plugin';
import pkg from 'eslint-config-xo';
const { rules: xo_rules } = pkg;

/** @type {import("eslint").Linter.FlatConfig[]} */
const config = [{
  // env: {
  //   browser: true,
  //   es2021: true,
  // },
  // extends: [
  //   'xo',
  //   'plugin:react/recommended',
  // ],
  // overrides: [
  //   {
  //     // env: {
  //     //   node: true,
  //     // },
  //     files: [
  //       'eslint.config.{js,cjs,mjs}',
  //     ],
  //     parserOptions: {
  //       sourceType: 'script',
  //     },
  //   },
  // ],
  languageOptions: {
    parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
},
  plugins: {
    react: react
  },
  rules: {
    indent: 'off',
    xo_rules,
  },
  ...react.configs.recommended
}];

export default config;
