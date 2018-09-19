export function paginatedStoreFactory () {
  return {
    currentPage: null, // Current Page number
    pagesCount: null, // Total Pages Count
    resultsCount: null, // Total Results Count
    results: [],
    pageSize: null, // Sorting By
    sortBy: null, // Sorting By
    searchTerm: null, // Search terms
    ascending: true
  }
}

export const setStorePageMutation = (context, Model) => (state, data) => {
  // update results
  state[context].results.splice(0, state[context].results.length)
  data.results.map(raw => {
    state[context].results.push(new Model(raw))
  })
  // update pagination data
  state[context].currentPage = data.page
  state[context].pagesCount = data.num_pages
  state[context].resultsCount = data.count
}
