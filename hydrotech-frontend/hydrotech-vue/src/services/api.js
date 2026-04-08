import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:8000',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default {
    // Rios
    getRios() {
        return apiClient.get('/rios/');
    },
    getRio(id) {
        return apiClient.get(`/rios/${id}`);
    },
    createRio(data) {
        return apiClient.post('/rios/', data);
    },
    updateRio(id, data) {
        return apiClient.put(`/rios/${id}`, data);
    },
    deleteRio(id) {
        return apiClient.delete(`/rios/${id}`);
    },

    // Usuarios
    getUsuarios() {
        return apiClient.get('/usuarios/');
    },
    getUsuario(id) {
        return apiClient.get(`/usuarios/${id}`);
    },
    createUsuario(data) {
        return apiClient.post('/usuarios/', data);
    },
    updateUsuario(id, data) {
        return apiClient.put(`/usuarios/${id}`, data);
    },
    deleteUsuario(id) {
        return apiClient.delete(`/usuarios/${id}`);
    },
};