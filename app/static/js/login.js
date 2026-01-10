function loginHandler() {
    return {
        formData: {
            usermail: '',
            password: ''
        },
        loading: false,
        async submitLogin() {
            this.loading = true;
            const backendResponse = await requestBackend('/api/auth/login','POST',this.formData)
            if (backendResponse != null){
                window.location.href = '/library';
            }
            this.loading = false;
        }
    }
}

