
import { dirname } from 'path';
import { fileURLToPath } from 'url';
import test from 'ava'
import { browserEnvConfig, loadConfiguration } from '../index.mjs'
import { join, resolve } from 'path'

test('can use a string', t => {
  const global = 'window document'
  t.deepEqual(browserEnvConfig(global), [['window', 'document']])
})

test('can use a plain array', t => {
  const global = ['window']
  t.deepEqual(browserEnvConfig(global), [global])
})

test('can use a plain object', t => {
  const jsdom = {a: 'hello'}
  t.deepEqual(browserEnvConfig(jsdom), [jsdom])
})

test('can use a named array', t => {
  const global = ['window']
  const config = global

  t.deepEqual(browserEnvConfig(config), [global])
})

test('can use a named object', t => {
  const jsdom = {a: 'hello'}
  const config = {jsdom}

  t.deepEqual(browserEnvConfig(config), [jsdom])
})

test('can use a config object', t => {
  const global = ['window']
  const jsdom = {a: 'hello'}
  const config = {globals: global, jsdom}

  t.deepEqual(browserEnvConfig(config), [global, jsdom])
})

test('can use none', t => {
  t.is(browserEnvConfig(), undefined)
})

test.serial('can load config', t => {
  const test_directory = dirname(fileURLToPath(import.meta.url));
  const config = loadConfiguration(join(test_directory, 'fixtures'))
  t.deepEqual(config, {ignore: {}})
})
