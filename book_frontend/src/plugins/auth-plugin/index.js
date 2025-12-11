// src/plugins/auth-plugin/index.js
module.exports = function authPlugin(context, options) {
  return {
    name: 'auth-plugin',
    // Using wrapRootElement to provide AuthProvider at the app root
    // This should wrap the entire React application, ensuring all components have access
    wrapRootElement: require.resolve('./client-modules/auth-wrapper.js'),
  };
};