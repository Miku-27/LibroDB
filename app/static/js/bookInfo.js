function bookInfoReactive(){ 
    return{
        async saveBookToggle(bookId){
            const methodToUse = this.booksaved ? 'DELETE' : 'POST';
            if (methodToUse === "DELETE"){
                if (!confirm('Delete this collection?')) return;
            }
            let url = `/api/library/books/${bookId}`
            let [status,data] = await requestBackend(url,methodToUse)
            if (!status){return;}
            this.booksaved = !this.booksaved;
        }
    } 
}