<template>
  <v-container fluid grid-list-lg>
    <v-layout class="px-2" v-if="sorting && sorting.length > 0">
      <v-layout row wrap>
        <v-flex sm10>
          <v-text-field label="Search" prepend-icon="search" v-model="search" />
        </v-flex>
        <v-flex sm2>
          <v-select return-object label="Sort By" prepend-icon="sort" :items="sorting" v-model="sort" />
        </v-flex>
      </v-layout>
    </v-layout>

    <template v-if="state.results.length > 0">
      <v-layout row wrap>
        <v-flex v-for="item in state.results" :key="item.pk" :class="[size]">
          <slot :item="item" />
        </v-flex>
      </v-layout>

      <v-layout row wrap align-center>
        <v-flex xs12 md2 class="text-xs-center text-md-left grey--text">
          Showing: {{ startRange }} - {{ endRange }} / {{ this.state.resultsCount }}
        </v-flex>
        <v-flex xs12 md8 class="text-xs-center">
          <v-pagination v-model="curretPage" :length="this.state.pagesCount" :total-visible="computedPagesVisible" />
        </v-flex>
        <v-flex xs12 md2 class="text-xs-center text-md-right grey--text">
          <v-select :items="avaiablePageSizes" v-model="options.size" label="Itens by Page" />
        </v-flex>
      </v-layout>
    </template>
    <template v-else>
      <v-layout column justify-center align-center>
        <logo-img />
        <v-subheader style="height: 20px">Ooops!</v-subheader>
        <p class="grey--text">Sorry, I couldn't find any data...</p>
      </v-layout>
    </template>
  </v-container>
</template>

<script>
import LogoImg from '@/components/LogoImg'
import { debounce } from '@/utils'

export default {
  name: 'PaginatedCardList',

  components: { LogoImg },

  data () {
    return {
      search: '',
      avaiablePageSizes: [4, 8, 12, 16, 20],
      options: { page: 1, size: null, sort: null, search: null }
    }
  },

  props: {
    size: { type: String, default: 'xs12' },
    action: { type: String, default: null },
    state: { type: Object, default: null },
    itensPerPage: {type: Number, default: 8},
    sorting: {type: Array, default: () => []},
    pagesVisible: {type: Number, default: 7}
  },

  computed: {
    sort: {
      get () {
        let sort = this.sorting.find(s => s.value === this.$route.query.sort)
        if (sort) return sort
        return this.sorting[0]
      },

      set (val) {
        let sort = this.sorting.find(s => s.value === val.value)
        if (sort) this.options.sort = sort.value
        else this.options.sort = this.sorting[0].value
      }
    },

    curretPage: {
      get () { return this.state.currentPage },
      set (val) { this.options.page = val }
    },

    startRange () {
      if (this.curretPage === 1) { return 1 }
      return ((this.curretPage - 1) * this.options.size) + 1
    },

    endRange () {
      if (this.curretPage === this.state.pagesCount) { return this.state.resultsCount }
      return this.curretPage * this.options.size
    },

    computedPagesVisible () { return this.$vuetify.breakpoint.xsOnly ? 5 : this.pagesVisible }
  },

  watch: {
    '$route.query': {
      handler (val) {
        this.options.page = this.$route.query.page
        this.options.sort = this.$route.query.sort
        this.options.size = this.$route.query.size
        this.options.search = this.$route.query.search
      },
      deep: true
    },

    search: debounce(function () {
      this.options.search = this.search
    }, 500),

    options: {
      handler (val) {
        if (
          this.options.page !== this.$route.query.page ||
          this.options.size !== this.$route.query.size ||
          this.options.search !== this.$route.query.search ||
          this.options.sort !== this.$route.query.sort
        ) {
          let query = {
            page: this.options.page,
            size: this.options.size,
            sort: this.options.sort,
            search: this.options.search
          }
          this.$router.push({ name: this.$route.name, query: query })
        }
        this.fetchData()
      },
      deep: true
    }
  },

  methods: {
    fetchData () { return this.$store.dispatch(this.action, this.options) }
  },

  created () {
    if (this.$route.query.page !== undefined) {
      this.options.page = this.$route.query.page
    }
    if (this.$route.query.search !== undefined) {
      this.options.search = this.$route.query.search
      this.search = this.$route.query.search
    }

    if (this.$route.query.sort !== undefined) {
      this.sort = {value: this.$route.query.sort}
    } else {
      this.sort = this.sorting[0]
    }
    if (this.$route.query.size !== undefined) {
      this.options.size = this.$route.query.size
    } else {
      this.options.size = this.itensPerPage
    }
  }
}
</script>
