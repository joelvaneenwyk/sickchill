function browserEnvConfig(config) {
  if (typeof config === 'string') {
    config = config.split(/(?:\s*,\s*)|\s+/)
  }

  const args = [
    config && Array.isArray(config) ? config : config && config.globals,
    config && !Array.isArray(config) && ((config && config.jsdom) || config)
  ].filter(x => x)
  return args.length > 0 ? args : undefined
}

function loadConfiguration(from) {
  const {searchSync} = require('cosmiconfig')('browser-env')
  const result = searchSync(from)
  return result && result.config
}

module.exports = require('browser-env').apply(
  this,
  browserEnvConfig(loadConfiguration())
)

Object.assign(module.exports, {
  browserEnvConfig,
  loadConfiguration
})
