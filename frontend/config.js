const isLocalStaticServer =
  ["127.0.0.1", "localhost"].includes(window.location.hostname) &&
  window.location.port === "5173";

window.APP_CONFIG = {
  API_BASE: isLocalStaticServer
    ? "http://127.0.0.1:8000/api"
    : `${window.location.origin}/api`
};
