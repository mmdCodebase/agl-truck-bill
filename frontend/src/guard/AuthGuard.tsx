import Cookies from "js-cookie";

type Props = {
  children: React.ReactNode;
};

const AuthGuard = ({ children }: Props) => {
  const accessToken = Cookies.get("access_token");

  if (!accessToken) {
    window.location.href = `${process.env.AUTH_SERVICE_URL}?redirect_url=${window.location.href}`;
    return null;
  } else {
    return <>{children}</>;
  }
};

export default AuthGuard;
