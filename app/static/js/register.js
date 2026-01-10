
document.addEventListener('alpine:init', () => {
    Alpine.data('registerHandlerReactive', () => ({
        formData: {
            username:'',
            usermail: '',
            password: ''
        },
        loading: false,
        async submitRegister() {
            this.loading = true;
            const backendResponse = await requestBackend('/api/auth/Register','POST',this.formData)
            if (backendResponse != null){
                window.location.href = '/login';
            }
            this.loading = false;
        }
    }))
})
