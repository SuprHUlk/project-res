import { get } from "./axios";

export const verifyAuth = async (): Promise<boolean> => {
    try {
        const res = await get("/auth/verify");
        return res.isSuccess;
    } catch (e) {
        console.error("Auth verification failed:", e);
        return false;
    }
};

export const checkAuthStatus = async (): Promise<boolean> => {
    return await verifyAuth();
};
