// Example push notification simulation
function showNotification(message) {
  var notif = document.createElement('div');
  notif.style.position = 'fixed';
  notif.style.bottom = '20px';
  notif.style.right = '20px';
  notif.style.background = '#D81324';
  notif.style.color = '#fff';
  notif.style.padding = '16px';
  notif.style.borderRadius = '8px';
  notif.style.boxShadow = '0 2px 8px rgba(0,0,0,0.2)';
  notif.innerText = message;
  document.body.appendChild(notif);
  setTimeout(function() { notif.remove(); }, 3000);
}
