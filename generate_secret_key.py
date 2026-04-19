#!/usr/bin/env python
"""
Script pour générer une SECRET_KEY Django sécurisée
Exécutez : python generate_secret_key.py
"""
import secrets
import string

def generate_secret_key():
    """Génère une SECRET_KEY Django sécurisée"""
    chars = string.ascii_letters + string.digits + string.punctuation
    # Django recommande au moins 50 caractères
    key = ''.join(secrets.choice(chars) for _ in range(64))
    return key

if __name__ == '__main__':
    secret_key = generate_secret_key()
    print("Votre SECRET_KEY sécurisée pour Render :")
    print(f"SECRET_KEY={secret_key}")
    print("\nCopiez cette valeur dans les variables d'environnement de Render.")