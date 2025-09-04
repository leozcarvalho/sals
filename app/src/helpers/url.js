export const refreshURL = (queryParams, ignoreFields=[]) => {
    let currentUrl = new URL(window.location.href);
    for (const key in queryParams) {
      if (queryParams.hasOwnProperty(key) && queryParams[key] && !ignoreFields.includes(key)) {
        currentUrl.searchParams.set(key, queryParams[key]);
      } else {
        currentUrl.searchParams.delete(key);
      }
    }
    window.history.pushState(null, null, currentUrl.toString());
}

export const parseQueryStringToObject = (queryString) => {
    const obj = {};
    const pairs = queryString.split('&');
  
    for (const pair of pairs) {
      const [key, value] = pair.split('=');
      obj[key] = decodeURIComponent(value);
    }
    return obj;
}

export const assingQueryString = (targetObject) => {
    const queryString = window.location.search.split('?');
    if (queryString.length > 1) {
      const obj = parseQueryStringToObject(queryString[1]);
      Object.assign(targetObject, obj)
    }
}

export const getQueryParam = (param) => {
  const url = window.location.href;
  const urlObj = new URL(url);
  const params = new URLSearchParams(urlObj.search);
  return params.get(param);
}

export const injectQueryParam = (param, value) => {
  const url = new URL(window.location.href);
  url.searchParams.set(param, value);
  window.history.replaceState(null, '', url);
}