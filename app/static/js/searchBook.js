function searchComp() {
    return {
        query: null,
        results: [],
        loading: false,
        
        async searchBooks() {
            if (!this.query) return;
            this.query = this.query.trim();
            this.loading = true;

            const [status,data] = await requestBackend(`/api/books?query=${encodeURIComponent(this.query)}`);
            if (!status){return;}
            this.results = (data || []).map(book => {
                if (book.thumbnail) {
                    book.thumbnail = book.thumbnail.replace('http://', 'https://');
                }
                return book;
            });
            this.loading = false;
        },
    }
}