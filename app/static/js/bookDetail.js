document.addEventListener('alpine:init', () => {
    Alpine.data('bookDetailReactive', ({ thumbnail, googleId, inLibrary }) => ({
       
        original: thumbnail,
        highRes: thumbnail.replace('zoom=1', 'zoom=3').replace('http://', 'https://'),
        triedHighRes: false,
        bookGoogleId: googleId,
        isInLibrary: inLibrary,
        
         
        async onImageError(){
            if (!this.triedHighRes) {
                this.triedHighRes = true;
                this.highRes = this.original;
            }
        },

        async saveBookToggle(){
            let url = `/api/library/books/${this.bookGoogleId}`
            let methodToUse = this.isInLibrary ? 'POST':'DELETE';
            if(this.isInLibrary){
                if (!confirm('Delete this collection?')) return;
            }
            let [status, data] = await requestBackend(url, methodToUse)
            if (!status) { return; }
            this.isInLibrary = !this.isInLibrary;
        },

        async saveBookToggle(bookId){
            const methodToUse = this.booksaved ? 'DELETE' : 'POST';
            if (methodToUse === "DELETE") {
                if (!confirm('Delete this collection?')) return;
            }
            let url = `/api/library/books/${bookId}`
            let [status, data] = await requestBackend(url, methodToUse)
            if (!status) { return; }
            this.booksaved = !this.booksaved;
        }
    }))
})
