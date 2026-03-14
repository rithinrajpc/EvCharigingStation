// QR code generation (using QRious)
function generateQRCode(text, elementId) {
  var qr = new QRious({
    element: document.getElementById(elementId),
    value: text,
    size: 150
  });
}
