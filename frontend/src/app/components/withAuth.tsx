"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { checkAuthStatus } from "../helpers/auth";

interface WithAuthProps {
    children?: React.ReactNode;
}

const withAuth = <P extends object>(
    WrappedComponent: React.ComponentType<P>
): React.FC<P & WithAuthProps> => {
    const AuthGuardedComponent: React.FC<P & WithAuthProps> = (props) => {
        const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(
            null
        );
        const [isLoading, setIsLoading] = useState(true);
        const router = useRouter();

        useEffect(() => {
            const verifyAuthentication = async () => {
                try {
                    const authStatus = await checkAuthStatus();
                    setIsAuthenticated(authStatus);

                    if (!authStatus) {
                        router.push("/login");
                    }
                } catch (error) {
                    console.error("Authentication check failed:", error);
                    setIsAuthenticated(false);
                    router.push("/login");
                } finally {
                    setIsLoading(false);
                }
            };

            verifyAuthentication();
        }, [router]);

        // Show loading state while checking authentication
        if (isLoading) {
            return (
                <div
                    style={{
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center",
                        height: "100vh",
                        fontSize: "18px",
                        color: "#666",
                    }}
                >
                    Loading...
                </div>
            );
        }

        // Don't render the component if not authenticated
        if (!isAuthenticated) {
            return null;
        }

        // Render the wrapped component if authenticated
        return <WrappedComponent {...props} />;
    };

    AuthGuardedComponent.displayName = `withAuth(${
        WrappedComponent.displayName || WrappedComponent.name
    })`;

    return AuthGuardedComponent;
};

export default withAuth;
