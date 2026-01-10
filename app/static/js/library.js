function library() {
    return {
      //grid related
      books: [],
      currentPage:1,
      totalPages:2,
      isCardLoading: false,

      activeMenuId : null,
      
      //control bar related 
      isCollectionDropdownOpen: false,
      collectionDropdownSelectedItem: "Library",
      selectedCollectionId:null,
      collections:[],

      //grid related func
      init() {
        const data = JSON.parse(document.getElementById('bootstrap-books').textContent);
        this.books = data.book_data.books;
        this.currentPage = data.book_data.page;
        this.totalPages = data.book_data.total_pages;

        this.collections = data.collection_data
      },
      
      async getBooks({page=1,limit=9,...filters} = {}){

        let params = new URLSearchParams();

        params.append('page', page);
        params.append('limit', limit);

        Object.entries(filters).forEach(([key, value]) => {
          if (value !== null && value !== '') {
              params.append(key, value);
          }
        });
        
        const url = `/api/library/books?${params.toString()}`;
        let [status,data] = await requestBackend(url,"GET");
        if (!status){return;}
        this.books = (data.books).map(book => {
            if (book.thumbnail) {
                book.thumbnail = book.thumbnail.replace('http://', 'https://');
            }
            return book;
        });
        this.currentPage = data.page;
        this.totalPages = data.total_pages;
      },

      async updateBookStatus(bookId,new_book_status){
        this.activeMenuId = null;
        let [status,data] = await requestBackend(`/api/library/books/${bookId}`,"PATCH",{new_status:new_book_status});
        if (!status){return;}
        this.books = this.books.map(b => b.id === bookId ? { ...b, status:new_book_status } : b);
      },

      async removeBook(bookId,type,collectionId) {
        // type could be 'collection' or 'library'

        if(!collectionId && type === 'collection'){
          customToastMessage('Choose a collection first from control bar',false)
          return
        }

        this.activeMenuId = null;
        const endpoint = type === 'library' ? `/api/library/books/${bookId}` : `/api/collections/${collectionId}/book/${bookId}`;
        if (!confirm(`Are you sure you want to remove this from your ${type}?`)) return;
        
        let [status, data] = await requestBackend(endpoint, 'DELETE');
        if (status) {
            this.books = this.books.filter(b => b.id !== bookId);
        }
      },

      openAddToCollection(bookId) {
        this.selectedBookId = bookId;
        this.modal = 'addToCollection';
      },
  

      async addBook(type,collectionId) {
        // type could be 'collection' or 'library'

        if(!collectionId && type === 'collection'){
          customToastMessage('Choose a collection first from modal',false)
          return
        }

        this.modal = null;
        const endpoint = type === 'library' ? `/api/library/books/${this.selectedBookId}` : `/api/collections/${collectionId}/book/${this.selectedBookId}`;
        this.selectedBookId = null;
        let [status, data] = await requestBackend(endpoint, 'POST');
      },

      //control bar related func

      // Filter related 
      isFilterDropdownOpen: false, 
      showLanguagesDropdown: false, 
      filters: { 
        googleId:null,
        title:null,
        authorName:null,
        status: null,
        collectionId:null,
        language: null,
        pageCountLt: null,
        pageCountMt: null,
        pageCountEq: null,
        publishedDate:null,
        publisher:null,
        isbn13:null,
        isbn10:null
      },

      //modal related data
    
      modal: null,
      newCollectionName: '',
      editingId: null,
      editName: '',
      selectedBookId : null,
    
      openCollections() {
          this.modal = 'collections';
          this.editingId = null;
          this.newCollectionName = '';
      },

      async addCollection() {
          if (!this.newCollectionName) return;
          let [status,data] = await requestBackend('/api/collections', 'POST', { collection_name: this.newCollectionName });
          if (!status){
            this.newCollectionName = '';
            return
          }
          this.newCollectionName = '';
      },
  
      async deleteCol(id) {
          if (!confirm('Delete this collection?')) return;
          let [status,data] = await requestBackend(`/api/collections/${id}`, 'DELETE');
          if (!status){return}
          this.collections = this.collections.filter(item => item.collection_id !== id);
      },
  
      async saveRename(id) {
          let [status,data] = await requestBackend(`/api/collections/${id}`, 'PATCH', { name: this.editName });
          if (!status){
            this.editingId = null;
            return
          }
          
          let item = this.collections.find(c => c.collection_id === id);
          if (item) item.collection_name = this.editName;

          this.editingId = null;
      }
    }
  }
  
