FROM node:20.6.1-alpine as build-stage

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

# WORKDIR /app/Vite
# RUN npm install @vue/cli -g
# COPY ./Vite/package.json .
# COPY ./Vite/package-lock.json .
COPY . ./

# EXPOSE 8080
# Change below to dev
# RUN npm run dev
WORKDIR /app/Vite
# CMD ["npm", "run", "dev"]
# RUN npm install @vue/cli -g
RUN npm install
RUN npm run build
# RUN npm run dev

FROM nginx:stable-alpine as production-stage 
COPY --from=build-stage /app/Vite/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 