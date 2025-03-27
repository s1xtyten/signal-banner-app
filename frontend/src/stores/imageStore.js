import { writable } from 'svelte/store';

export const imageSettings = writable({
    cropArea: { x: 0, y: 0, width: 100, height: 100 },
    bannerOpacity: 0.8,
    bannerPosition: 50 // percentage from top
});