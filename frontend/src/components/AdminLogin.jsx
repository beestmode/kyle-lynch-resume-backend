import React, { useState } from 'react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { X, LogIn, Shield } from 'lucide-react';
import { useAuth } from './AuthContext';

const AdminLogin = ({ onClose, onSuccess }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const result = await login(credentials);
      if (result.success) {
        onSuccess?.();
        onClose();
      }
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <Card className="w-full max-w-md bg-gradient-to-br from-yellow-50 via-amber-50 to-orange-100 border-2 border-amber-200 shadow-2xl">
        <div className="p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-amber-900 flex items-center gap-2">
              <Shield className="w-6 h-6" />
              Admin Access
            </h2>
            <Button
              variant="ghost"
              size="sm"
              onClick={onClose}
              className="text-amber-600 hover:text-amber-800 hover:bg-amber-100"
            >
              <X className="w-5 h-5" />
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Label htmlFor="username" className="text-amber-800 font-medium">
                Username
              </Label>
              <Input
                id="username"
                name="username"
                value={credentials.username}
                onChange={handleChange}
                required
                autoComplete="username"
                className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                placeholder="Enter admin username"
              />
            </div>

            <div>
              <Label htmlFor="password" className="text-amber-800 font-medium">
                Password
              </Label>
              <Input
                id="password"
                name="password"
                type="password"
                value={credentials.password}
                onChange={handleChange}
                required
                autoComplete="current-password"
                className="border-amber-300 focus:border-amber-500 bg-amber-50/50"
                placeholder="Enter admin password"
              />
            </div>

            <div className="flex gap-3 pt-4">
              <Button
                type="submit"
                disabled={isLoading || !credentials.username || !credentials.password}
                className="flex-1 bg-amber-700 hover:bg-amber-800 text-cream"
              >
                <LogIn className="w-4 h-4 mr-2" />
                {isLoading ? 'Signing In...' : 'Sign In'}
              </Button>
              <Button
                type="button"
                variant="outline"
                onClick={onClose}
                className="border-amber-600 text-amber-800 hover:bg-amber-100"
              >
                Cancel
              </Button>
            </div>
          </form>

          <div className="mt-6 pt-4 border-t border-amber-200">
            <p className="text-sm text-amber-600 text-center">
              Admin access is required to edit resume content
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default AdminLogin;