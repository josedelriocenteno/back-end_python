# Firmas de Commits: Verificando la autoría

En entornos de alta seguridad o proyectos Open Source importantes, no basta con decir quién eres; debes demostrarlo mediante criptografía.

## 1. El problema de la suplantación
Cualquiera puede configurar su Git local con `user.name "Elon Musk"`. GitHub mostrará su cara en el commit, pero eso no significa que el commit sea suyo.

## 2. Firmas GPG (GnuPG)
Al firmar un commit con una clave GPG, GitHub muestra un check verde de **"Verified"**.
- Esto asegura que el commit proviene de una persona que posee una clave privada específica vinculada a su cuenta.

## 3. Configuración básica
1. Generas una clave GPG en tu ordenador.
2. Subes la clave pública a tu perfil de GitHub.
3. Configuras Git para firmar: 
   `git config --global commit.gpgsign true`
   `git config --global user.signingkey <TU_ID_DE_CLAVE>`

## 4. Firmas con SSH (Más moderno y simple)
GitHub ahora permite usar tu misma clave SSH (la que usas para hacer push) para firmar los commits. Es mucho más sencillo de configurar que GPG.
`git config --global gpg.format ssh`
`git config --global user.signingkey ~/.ssh/id_ed25519.pub`

## 5. Vigilant Mode (Modo Vigilante)
Activa esto en GitHub para que cualquier commit que NO esté firmado aparezca como "Unverified". Esto ayuda a detectar si alguien está intentando subir código en tu nombre sin tu permiso.

## Resumen: Identidad Digital
Firmar tus commits es la marca de un profesional preocupado por la integridad del código. En muchas empresas tecnológicas modernas, es un requisito obligatorio por motivos de cumplimiento (compliance) y seguridad.
