// webpack.config.js
const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  entry: {
    app: "./django/assets/js/viewer.js",   // tu entrada principal de JS
    login_intro: "./django/assets/js/login_intro.js",
    styles: "./django/assets/scss/main.scss",
  },
  output: {
    filename: "bundles/[name].bundle.js",
    path: path.resolve(__dirname, "static_build"), // salida para collectstatic
    clean: true, // limpia antes de cada build (solo dentro de static/)
  },
  module: {
    rules: [
      {
        test: /\.s?css$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.(png|jpe?g|gif|svg)$/i,
        type: "asset/resource",
        generator: {
          filename: "images/[name][ext]", // imágenes → static/images/
        },
      },
      {
        test: /\.(woff2?|eot|ttf|otf)$/i,
        type: "asset/resource",
        generator: {
          filename: "fonts/[name][ext]", // fuentes → static/fonts/
        },
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "bundles/[name].css",
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "django/assets/images"),
          to: "images", // copia imágenes crudas → static/images/
          noErrorOnMissing: true,
        },
      ],
    }),
  ],
  resolve: {
    extensions: [".js", ".jsx", ".scss"],
  },
  devtool: "source-map",
  mode: "development", // cámbialo a "production" en despliegue
};
