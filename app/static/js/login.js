function loginHandler() {
    return {
        formData: {
            usermail: '',
            password: ''
        },
        loading: false,
        async submitLogin() {
            this.loading = true;
            const [status,data] = await requestBackend('/api/auth/token','POST',this.formData)
            if (status){
                window.location.href = '/library';
            }
            this.loading = false;
        },
    }
}

