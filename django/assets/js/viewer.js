const options = {
  env: 'AutodeskProduction',
  accessToken: window.forgeConfig.token
};

Autodesk.Viewing.Initializer(options, () => {
  const viewerDiv = document.getElementById('forgeViewer');
  const viewer = new Autodesk.Viewing.GuiViewer3D(viewerDiv);
  viewer.start();

  Autodesk.Viewing.Document.load(
    `urn:${window.forgeConfig.urn}`,
    doc => {
      const defaultModel = doc.getRoot().getDefaultGeometry();
      viewer.loadDocumentNode(doc, defaultModel);
    },
    error => console.error(error)
  );
});
