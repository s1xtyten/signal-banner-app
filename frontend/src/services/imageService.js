import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:5000';

export const uploadImage = async (file, settings = {}) => {  // Add default settings
    const formData = new FormData();
    formData.append('image', file);
    formData.append('settings', JSON.stringify({
        bannerOpacity: settings.bannerOpacity ?? 0.8,
        bannerPosition: settings.bannerPosition ?? 50,
        cropArea: settings.cropArea ?? null
    }));
    
    const response = await axios({
        method: 'post',
        url: `${API_BASE_URL}/api/upload`,
        data: formData,
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        withCredentials: true
    });
    
    return response.data;
};