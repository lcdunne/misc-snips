const formToJSON = (form) => {
  // Converts x-www-form-urlencoded data from a form element into a JSON object
  return Object.fromEntries(new FormData(form));
};

const makeRequest = async (method, url, body, extraHeaders = {}) => {
  // Generic function to make an asynchronous request
  try {
    const response = await fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json", ...extraHeaders },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      // For HTTP error responses (promise resolved, but HTTP error)
      return handleErrors(response);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    // In case we cannot reach the server (promise rejected)
    console.error(error);
  }
};
