function registerHandler() {
    return {
        formData: {
            username:'',
            usermail: '',
            password: ''
        },
        loading: false,
        async submitRegister() {
            this.loading = true;
            const backendResponse = await requestBackend('/api/auth/register','POST',this.formData)
            if (backendResponse != null){
                window.location.href = '/login';
            }
            this.loading = false;
        }
    }
}

