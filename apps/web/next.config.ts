import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // 워크스페이스 패키지는 TS 소스 그대로 배포되므로 Next가 직접 트랜스파일한다.
  transpilePackages: ["@team2/shared", "@team2/ui"],
  cacheComponents: true,
  partialPrefetching: true,
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
