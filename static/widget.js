!(function () {
  function t() {
    var t = document.createElement("iframe");
    (t.title = "Scanning alert"),
      t.setAttribute(
        "style",
        "width:100%!important;height:100%!important;position:fixed!important;left:0!important;right:0!important;top:0!important;bottom:0!important;z-index:999999"
      ),
      document.body.appendChild(t),
      (t.src = n + "scan_error.html");
  }
  try {
    var e = document.getElementsByTagName("html")[0],
      i = "data-uw-w-loader";
    if (e && e.hasAttribute(i)) return;
    e.setAttribute(i, "");
  } catch (t) {}
  var n = "https://cdn.userway.org/widgetapp/",
    a = n + "2021-11-26/widget_app_base_1637931784622.js",
    o = n + "2021-11-26/widget_app_1637931784622.js";
  if (
    (location.origin && location.origin.indexOf(".webaim.") > -1) ||
    (location.origin && location.origin.indexOf("acsbace") > -1)
  )
    setTimeout(function () {
      t();
    }, 1e3);
  else {
    if (!new RegExp("(bot|crawler)", "i").test(navigator.userAgent)) {
      var r = window._userway_config;
      (navigator.userAgent.match(/mobile/i) &&
        r &&
        ("false" === r.mobile || !1 === r.mobile)) ||
        ((function () {
          try {
            (UserWayWidgetApp = {}),
              (Object.keys(localStorage).filter(function (t) {
                return 0 === t.indexOf("userway-s");
              }).length > 0 ||
                /Edge\/|Trident\/|MSIE/.test(navigator.userAgent)) &&
                ((a = o), (UserWayWidgetApp.lazyLoaded = !0));
          } catch (t) {}
        })(),
        (function (t, e) {
          var i = document.body || document.head,
            n = document.createElement("script");
          (n.onload = function () {
            e && e();
          }),
            (n.src = t),
            (n.id = "a11yWidgetSrc"),
            i.appendChild(n);
        })(a));
    }
  }
})();
