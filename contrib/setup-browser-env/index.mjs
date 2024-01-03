/**
 *
 */

import browserEnv from 'browser-env';
import {cosmiconfigSync} from 'cosmiconfig';

export function browserEnvConfig(config) {
  if (typeof config === 'string') {
    config = config.split(/(?:\s*,\s*)|\s+/);
  }

  const args = [
    config && Array.isArray(config) ? config : config && config.globals,
    config && !Array.isArray(config) && ((config && config.jsdom) || config),
  ].filter(Boolean);
  return args.length > 0 ? args : undefined;
}

export function loadConfiguration(from) {
  const result = cosmiconfigSync('browser-env').search(from);
  return result && result.config;
}

export const current_browser_env = browserEnv.apply(this, browserEnvConfig(loadConfiguration()));
