-- MariaDB initialization script for Data Pragyan application

-- Sample table for employees
CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department VARCHAR(50),
    salary DECIMAL(10,2),
    hire_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample table for departments
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    manager_id INT,
    budget DECIMAL(12,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample table for projects
CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    status ENUM('planning', 'active', 'completed', 'cancelled') DEFAULT 'planning',
    department_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Sample table for sales
CREATE TABLE IF NOT EXISTS sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    sale_amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    customer_name VARCHAR(100),
    region VARCHAR(50),
    salesperson_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data for employees
INSERT INTO employees (first_name, last_name, email, department, salary, hire_date) VALUES
('John', 'Doe', 'john.doe@company.com', 'Engineering', 75000.00, '2023-01-15'),
('Jane', 'Smith', 'jane.smith@company.com', 'Marketing', 65000.00, '2023-02-20'),
('Bob', 'Johnson', 'bob.johnson@company.com', 'Sales', 60000.00, '2023-03-10'),
('Alice', 'Brown', 'alice.brown@company.com', 'Engineering', 80000.00, '2022-11-05'),
('Charlie', 'Wilson', 'charlie.wilson@company.com', 'HR', 55000.00, '2023-04-12'),
('Diana', 'Davis', 'diana.davis@company.com', 'Finance', 70000.00, '2022-12-18'),
('Eva', 'Garcia', 'eva.garcia@company.com', 'Engineering', 82000.00, '2023-01-08'),
('Frank', 'Miller', 'frank.miller@company.com', 'Marketing', 58000.00, '2023-05-22'),
('Grace', 'Taylor', 'grace.taylor@company.com', 'Sales', 62000.00, '2023-02-14'),
('Henry', 'Anderson', 'henry.anderson@company.com', 'Engineering', 78000.00, '2022-10-30');

-- Insert sample data for departments
INSERT INTO departments (name, description, budget) VALUES
('Engineering', 'Software development and technical operations', 500000.00),
('Marketing', 'Brand promotion and customer acquisition', 200000.00),
('Sales', 'Revenue generation and customer relations', 300000.00),
('HR', 'Human resources and employee management', 150000.00),
('Finance', 'Financial planning and accounting', 180000.00);

-- Insert sample data for projects
INSERT INTO projects (name, description, start_date, end_date, budget, status, department_id) VALUES
('Mobile App Development', 'Create a mobile application for customers', '2023-01-01', '2023-06-30', 150000.00, 'active', 1),
('Marketing Campaign Q2', 'Digital marketing campaign for Q2', '2023-04-01', '2023-06-30', 75000.00, 'active', 2),
('Sales Automation', 'Implement CRM and sales automation tools', '2023-02-15', '2023-08-15', 100000.00, 'active', 3),
('Website Redesign', 'Complete overhaul of company website', '2023-03-01', '2023-07-31', 80000.00, 'planning', 1),
('Employee Training Program', 'Comprehensive training for all employees', '2023-01-15', '2023-12-31', 50000.00, 'active', 4);

-- Insert sample data for sales
INSERT INTO sales (product_name, category, sale_amount, sale_date, customer_name, region, salesperson_id) VALUES
('Product A', 'Electronics', 1250.00, '2023-01-15', 'ABC Corp', 'North', 3),
('Product B', 'Software', 2500.00, '2023-01-18', 'XYZ Inc', 'South', 9),
('Product A', 'Electronics', 1250.00, '2023-01-22', 'DEF Ltd', 'East', 3),
('Product C', 'Services', 3750.00, '2023-01-25', 'GHI Company', 'West', 9),
('Product B', 'Software', 2500.00, '2023-02-02', 'JKL Enterprises', 'North', 3),
('Product D', 'Hardware', 1875.00, '2023-02-05', 'MNO Solutions', 'South', 9),
('Product A', 'Electronics', 1250.00, '2023-02-08', 'PQR Group', 'East', 3),
('Product C', 'Services', 3750.00, '2023-02-12', 'STU Systems', 'West', 9),
('Product E', 'Consulting', 5000.00, '2023-02-15', 'VWX Technologies', 'North', 3),
('Product B', 'Software', 2500.00, '2023-02-18', 'YZ Industries', 'South', 9);

-- Additional comprehensive test tables

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(50),
    industry VARCHAR(50),
    customer_since DATE,
    status ENUM('active', 'inactive', 'prospect') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    subcategory VARCHAR(50),
    description TEXT,
    price DECIMAL(10,2),
    cost DECIMAL(10,2),
    stock_quantity INT DEFAULT 0,
    min_stock_level INT DEFAULT 10,
    supplier VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(12,2),
    discount_amount DECIMAL(10,2) DEFAULT 0.00,
    tax_amount DECIMAL(10,2) DEFAULT 0.00,
    shipping_cost DECIMAL(10,2) DEFAULT 0.00,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    payment_method ENUM('credit_card', 'bank_transfer', 'cash', 'check') DEFAULT 'credit_card',
    shipping_address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
);

-- Employee performance table
CREATE TABLE IF NOT EXISTS employee_performance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    review_period VARCHAR(20),
    performance_score DECIMAL(3,2), -- Score out of 5.00
    goals_met INT DEFAULT 0,
    total_goals INT DEFAULT 0,
    manager_feedback TEXT,
    employee_feedback TEXT,
    review_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
);

-- Marketing campaigns table
CREATE TABLE IF NOT EXISTS marketing_campaigns (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    campaign_type ENUM('email', 'social_media', 'ppc', 'content', 'event') NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12,2),
    actual_spend DECIMAL(12,2) DEFAULT 0.00,
    target_audience VARCHAR(100),
    impressions INT DEFAULT 0,
    clicks INT DEFAULT 0,
    conversions INT DEFAULT 0,
    revenue_generated DECIMAL(12,2) DEFAULT 0.00,
    status ENUM('planning', 'active', 'paused', 'completed') DEFAULT 'planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Website analytics table
CREATE TABLE IF NOT EXISTS website_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    page_views INT DEFAULT 0,
    unique_visitors INT DEFAULT 0,
    bounce_rate DECIMAL(5,2), -- Percentage
    avg_session_duration TIME, -- in HH:MM:SS format
    new_users INT DEFAULT 0,
    returning_users INT DEFAULT 0,
    mobile_users INT DEFAULT 0,
    desktop_users INT DEFAULT 0,
    tablet_users INT DEFAULT 0,
    top_page VARCHAR(255),
    traffic_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample customers
INSERT INTO customers (company_name, contact_person, email, phone, city, state, country, industry, customer_since, status) VALUES
('TechCorp Solutions', 'Sarah Johnson', 'sarah@techcorp.com', '+1-555-0101', 'San Francisco', 'CA', 'USA', 'Technology', '2022-03-15', 'active'),
('Global Manufacturing Inc', 'Mike Chen', 'mike.chen@globalman.com', '+1-555-0102', 'Detroit', 'MI', 'USA', 'Manufacturing', '2021-07-22', 'active'),
('Healthcare Plus', 'Dr. Emily Rodriguez', 'emily@healthplus.com', '+1-555-0103', 'Miami', 'FL', 'USA', 'Healthcare', '2022-11-08', 'active'),
('EduTech Institute', 'James Wilson', 'james@edutech.edu', '+1-555-0104', 'Boston', 'MA', 'USA', 'Education', '2023-01-12', 'active'),
('RetailMax Corp', 'Lisa Zhang', 'lisa@retailmax.com', '+1-555-0105', 'Chicago', 'IL', 'USA', 'Retail', '2022-09-30', 'active'),
('FinanceFirst Bank', 'Robert Taylor', 'robert@financefirst.com', '+1-555-0106', 'New York', 'NY', 'USA', 'Finance', '2021-12-05', 'active'),
('GreenEnergy Solutions', 'Maria Garcia', 'maria@greenenergy.com', '+1-555-0107', 'Austin', 'TX', 'USA', 'Energy', '2023-02-18', 'prospect'),
('FoodService Pro', 'David Kim', 'david@foodservice.com', '+1-555-0108', 'Seattle', 'WA', 'USA', 'Food Service', '2022-06-14', 'active'),
('ConsultingExperts LLC', 'Jennifer Brown', 'jennifer@consultexp.com', '+1-555-0109', 'Denver', 'CO', 'USA', 'Consulting', '2023-04-03', 'active'),
('LogisticsTrans Inc', 'Carlos Mendez', 'carlos@logisticstrans.com', '+1-555-0110', 'Phoenix', 'AZ', 'USA', 'Logistics', '2022-08-27', 'inactive');

-- Insert sample products
INSERT INTO products (name, category, subcategory, description, price, cost, stock_quantity, supplier, is_active) VALUES
('Enterprise Software License', 'Software', 'Business', 'Annual license for enterprise software suite', 12000.00, 3000.00, 100, 'SoftwarePro Inc', TRUE),
('Cloud Storage Premium', 'Software', 'Infrastructure', 'Premium cloud storage solution - 1TB', 299.99, 89.99, 500, 'CloudTech Solutions', TRUE),
('Security Consultation', 'Services', 'Consulting', 'Comprehensive security audit and consultation', 5500.00, 1650.00, 0, 'Internal', TRUE),
('Data Analytics Platform', 'Software', 'Analytics', 'Advanced data analytics and visualization platform', 8900.00, 2670.00, 50, 'AnalyticsCorp', TRUE),
('Training Workshop', 'Services', 'Education', 'Professional development workshop (per person)', 750.00, 225.00, 0, 'Internal', TRUE),
('Hardware Server', 'Hardware', 'Servers', 'High-performance server for data processing', 15500.00, 9300.00, 25, 'ServerTech Ltd', TRUE),
('Mobile App Development', 'Services', 'Development', 'Custom mobile application development', 25000.00, 7500.00, 0, 'Internal', TRUE),
('Database License', 'Software', 'Database', 'Enterprise database management system license', 18000.00, 5400.00, 75, 'DatabasePro', TRUE),
('Network Equipment', 'Hardware', 'Networking', 'Enterprise network infrastructure package', 8750.00, 5250.00, 30, 'NetworkSystems Inc', TRUE),
('Support Package Premium', 'Services', 'Support', '24/7 premium support package (annual)', 3600.00, 1080.00, 0, 'Internal', TRUE);

-- Insert sample orders
INSERT INTO orders (customer_id, order_date, total_amount, discount_amount, tax_amount, status, payment_method) VALUES
(1, '2023-01-15', 15750.00, 750.00, 1260.00, 'delivered', 'credit_card'),
(2, '2023-01-18', 28900.00, 1400.00, 2199.00, 'delivered', 'bank_transfer'),
(3, '2023-01-22', 6200.00, 0.00, 496.00, 'shipped', 'credit_card'),
(4, '2023-01-25', 12000.00, 600.00, 912.00, 'processing', 'bank_transfer'),
(5, '2023-02-02', 4850.00, 0.00, 388.00, 'delivered', 'credit_card'),
(1, '2023-02-05', 8900.00, 0.00, 712.00, 'cancelled', 'credit_card'),
(6, '2023-02-08', 21600.00, 1080.00, 1641.60, 'delivered', 'bank_transfer'),
(7, '2023-02-12', 5500.00, 0.00, 440.00, 'pending', 'credit_card'),
(8, '2023-02-15', 9450.00, 450.00, 720.00, 'shipped', 'bank_transfer'),
(3, '2023-02-18', 18000.00, 900.00, 1368.00, 'processing', 'credit_card');

-- Insert sample order items
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
(1, 1, 1, 12000.00, 12000.00), (1, 5, 2, 750.00, 1500.00), (1, 2, 8, 299.99, 2399.92),
(2, 7, 1, 25000.00, 25000.00), (2, 10, 1, 3600.00, 3600.00),
(3, 3, 1, 5500.00, 5500.00), (3, 5, 1, 750.00, 750.00),
(4, 1, 1, 12000.00, 12000.00),
(5, 9, 1, 8750.00, 8750.00), (5, 5, 6, 750.00, 4500.00),
(6, 4, 1, 8900.00, 8900.00),
(7, 8, 1, 18000.00, 18000.00), (7, 10, 1, 3600.00, 3600.00),
(8, 3, 1, 5500.00, 5500.00),
(9, 6, 1, 15500.00, 15500.00), (9, 2, 15, 299.99, 4499.85),
(10, 8, 1, 18000.00, 18000.00);

-- Insert employee performance data
INSERT INTO employee_performance (employee_id, review_period, performance_score, goals_met, total_goals, review_date) VALUES
(1, '2023-Q1', 4.2, 8, 10, '2023-04-15'),
(2, '2023-Q1', 4.5, 9, 10, '2023-04-18'),
(3, '2023-Q1', 3.8, 7, 10, '2023-04-20'),
(4, '2023-Q1', 4.7, 10, 10, '2023-04-22'),
(5, '2023-Q1', 4.0, 8, 10, '2023-04-25'),
(6, '2023-Q1', 4.3, 9, 10, '2023-04-28'),
(7, '2023-Q1', 4.6, 9, 10, '2023-05-02'),
(8, '2023-Q1', 3.9, 7, 10, '2023-05-05'),
(9, '2023-Q1', 4.1, 8, 10, '2023-05-08'),
(10, '2023-Q1', 4.4, 9, 10, '2023-05-10');

-- Insert marketing campaigns
INSERT INTO marketing_campaigns (name, campaign_type, start_date, end_date, budget, actual_spend, impressions, clicks, conversions, revenue_generated, status) VALUES
('Spring Product Launch', 'email', '2023-03-01', '2023-03-31', 15000.00, 14250.00, 125000, 8500, 420, 185000.00, 'completed'),
('Social Media Boost Q2', 'social_media', '2023-04-01', '2023-06-30', 25000.00, 18750.00, 450000, 22500, 1125, 425000.00, 'active'),
('Google Ads Campaign', 'ppc', '2023-01-15', '2023-04-15', 30000.00, 28900.00, 850000, 42500, 2975, 892000.00, 'completed'),
('Content Marketing Initiative', 'content', '2023-02-01', '2023-08-31', 20000.00, 12000.00, 200000, 15000, 750, 225000.00, 'active'),
('Trade Show Participation', 'event', '2023-05-15', '2023-05-17', 50000.00, 47500.00, 5000, 250, 85, 340000.00, 'completed');

-- Insert website analytics data
INSERT INTO website_analytics (date, page_views, unique_visitors, bounce_rate, avg_session_duration, new_users, returning_users, mobile_users, desktop_users, tablet_users, top_page, traffic_source) VALUES
('2023-01-01', 2850, 1920, 34.5, '00:03:45', 1150, 770, 1425, 1140, 285, '/products', 'organic'),
('2023-01-02', 3200, 2140, 32.1, '00:04:12', 1280, 860, 1600, 1280, 320, '/services', 'direct'),
('2023-01-03', 2950, 1980, 35.8, '00:03:38', 1180, 800, 1475, 1180, 295, '/about', 'social'),
('2023-01-04', 3100, 2070, 33.2, '00:04:05', 1240, 830, 1550, 1240, 310, '/products', 'paid'),
('2023-01-05', 3350, 2240, 31.5, '00:04:28', 1340, 900, 1675, 1340, 335, '/contact', 'referral'),
('2023-01-06', 2800, 1870, 36.4, '00:03:22', 1120, 750, 1400, 1120, 280, '/blog', 'organic'),
('2023-01-07', 2700, 1800, 37.1, '00:03:15', 1080, 720, 1350, 1080, 270, '/services', 'direct'),
('2023-01-08', 3400, 2270, 30.8, '00:04:35', 1360, 910, 1700, 1360, 340, '/products', 'social'),
('2023-01-09', 3250, 2170, 32.6, '00:04:18', 1300, 870, 1625, 1300, 325, '/pricing', 'paid'),
('2023-01-10', 3150, 2100, 33.9, '00:04:02', 1260, 840, 1575, 1260, 315, '/demo', 'organic');

COMMIT;