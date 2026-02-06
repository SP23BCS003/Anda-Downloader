import { writable, derived, readable } from 'svelte/store';
import { browser } from '$app/environment';

// Language definitions
export const languages = {
    en: 'English',
    zh: '中文',
    es: 'Español',
    ar: 'العربية',
    hi: 'हिन्दी',
    fr: 'Français',
    pt: 'Português',
    bn: 'বাংলা',
    ru: 'Русский',
    ja: '日本語',
    de: 'Deutsch',
    ko: '한국어',
    it: 'Italiano',
    tr: 'Türkçe',
    vi: 'Tiếng Việt'
};

function getSavedLanguage(): string {
    if (browser) {
        return localStorage.getItem('language') || 'en';
    }
    return 'en';
}

export const currentLanguage = writable(getSavedLanguage());

// Translation store that holds the current translations
export const translations = writable<any>({});

// Load translations dynamically
async function loadTranslations(lang: string): Promise<any> {
    try {
        const module = await import(`./locales/${lang}.json`);
        return module.default || module;
    } catch (e) {
        console.warn(`Failed to load translations for ${lang}, falling back to English`);
        if (lang !== 'en') {
            try {
                const module = await import(`./locales/en.json`);
                return module.default || module;
            } catch (err) {
                console.error('Failed to load English translations', err);
                return {};
            }
        }
        return {};
    }
}

// Subscribe to language changes and load translations
currentLanguage.subscribe(async (lang) => {
    const trans = await loadTranslations(lang);
    translations.set(trans);
});

// Initialize with saved language
if (browser) {
    loadTranslations(getSavedLanguage()).then(trans => {
        translations.set(trans);
    });
}

// Helper function to get nested translation
export function t(translations: any, key: string): string {
    if (!translations || typeof translations !== 'object') {
        return key;
    }

    const keys = key.split('.');
    let result = translations;

    for (const k of keys) {
        if (result && typeof result === 'object') {
            result = result[k];
        } else {
            return key;
        }
    }

    return typeof result === 'string' ? result : key;
}

// Change language function
export function setLanguage(lang: string) {
    if (languages[lang as keyof typeof languages]) {
        currentLanguage.set(lang);
        if (browser) {
            localStorage.setItem('language', lang);
        }
    }
}
