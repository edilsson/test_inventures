FROM node:18-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm config set legacy-peer-deps true
RUN npm install --frozen-lockfile
COPY . .
RUN npm run build

FROM nginx:stable-alpine AS production
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]