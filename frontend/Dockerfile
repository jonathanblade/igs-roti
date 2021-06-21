FROM node:16-alpine AS base
ENV APP_HOME="/igs-roti-frontend"

FROM base AS dev
WORKDIR $APP_HOME
COPY package*.json ./
RUN npm install
COPY public public
COPY src src
COPY babel.config.js babel.config.js
COPY vue.config.js vue.config.js

FROM dev AS build
RUN npm run build

FROM nginx:1.18-alpine AS prod
COPY --from=build /igs-roti-frontend/dist /var/www/html
COPY ./etc/nginx.conf /etc/nginx/conf.d/default.conf
CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && \
    nginx -g 'daemon off;'
