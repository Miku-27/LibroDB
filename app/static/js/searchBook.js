document.addEventListener('alpine:init', () => {
    Alpine.data('searchCompReactive', () => ({
        query: null,
        results: [],
        loading: false,
        
        async searchBooks() {
            if (!this.query) return;
            this.query = this.query.trim();
            this.loading = true;

            const [status,data] = await requestBackend(`/api/books?query=${encodeURIComponent(this.query)}`);
            console.log(data);
            if (!status){return;}
            this.results = data || [];
            this.loading = false;
        },
    }))
})
