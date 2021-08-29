/**
 * HTTP get request
 * @param url
 * @param queryParams
 * @param headers
 * @returns {Promise<{body: any, status: number}>}
 */
export const getRequest = async (url, queryParams, headers) => {
  const response = await fetch(
    `${url}?${new URLSearchParams(queryParams).toString()}`,
    {
      method: 'GET',
      mode: 'cors',
      headers: {
        ...headers
      }
    }
  )
  return { status: response.status, body: await response.json() }
}

/**
 * HTTP post request
 * @param url
 * @param body
 * @param headers
 * @returns {Promise<{body: any, status: number}>}
 */
export const postRequest = async (url, body, headers) => {
  const response = await fetch(
    `${url}`,
    {
      method: 'POST',
      mode: 'cors',
      headers: {
        ...headers,
        'Content-type': 'application/json'
      },
      body: JSON.stringify(body)
    }
  )
  return { status: response.status, body: await response.json() }
}
