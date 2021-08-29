FROM node:14.17.5 as build

WORKDIR /frontend
ENV PATH /frontend/node_modules/.bin:$PATH
COPY package.json /frontend/package.json
RUN npm install --silent
COPY . /frontend
RUN npm run build

FROM nginx:1.16.0-alpine
COPY --from=build /frontend/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
CMD ["nginx", "-g", "daemon off;"]
