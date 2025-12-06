// Personalization plugin for handling skill level buttons

module.exports = function personalizationPlugin(context, options) {
  return {
    name: 'personalization-plugin',
    getClientModules() {
      return [require.resolve('./client-modules/personalization.js')];
    },
  };
};