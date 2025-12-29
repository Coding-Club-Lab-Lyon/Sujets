#!/usr/bin/env python3
"""
Race Timmy - 3D Racing Simulation
Cobra (Reference Implementation)
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
import time

from car_controller import CarController


class LidarSensor:
    """Simulates a LIDAR sensor with 90-degree field of view"""

    def __init__(self, range_max=50.0):
        self.range_max = range_max
        self.num_rays = 91  # -45 to +45 degrees, inclusive
        self.angles = np.linspace(-45, 45, self.num_rays)

    def scan(self, car_pos, car_angle, track):
        """
        Returns list of 91 distances from -45° to +45°
        car_pos: (x, y) position
        car_angle: rotation in degrees
        track: Track object with walls
        """
        distances = []

        for angle_offset in self.angles:
            # Calculate ray direction
            ray_angle = math.radians(car_angle + angle_offset)
            ray_dir = np.array([math.cos(ray_angle), math.sin(ray_angle)])

            # Cast ray and find intersection with track walls
            distance = self._cast_ray(car_pos, ray_dir, track)
            distances.append(min(distance, self.range_max))

        return distances

    def _cast_ray(self, origin, direction, track):
        """Cast a ray and return distance to nearest wall"""
        min_distance = self.range_max

        for wall in track.walls:
            distance = self._ray_segment_intersection(origin, direction, wall)
            if distance is not None and distance < min_distance:
                min_distance = distance

        return min_distance

    def _ray_segment_intersection(self, ray_origin, ray_dir, segment):
        """Calculate intersection between ray and line segment"""
        p1, p2 = segment
        v1 = ray_origin - p1
        v2 = p2 - p1
        v3 = np.array([-ray_dir[1], ray_dir[0]])

        denom = np.dot(v2, v3)
        if abs(denom) < 1e-6:
            return None

        # Use 2D cross product manually to avoid numpy warning
        t1 = (v2[0] * v1[1] - v2[1] * v1[0]) / denom
        t2 = np.dot(v1, v3) / denom

        if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
            return t1

        return None


class Track:
    """Race track with walls"""

    def __init__(self):
        # Define track as a series of wall segments (outer and inner boundaries)
        # Simple oval track
        self.walls = []
        self._create_oval_track()

        # Two-checkpoint system for lap completion
        # Checkpoint 1: Start/finish line at bottom (where car starts at x=0, y=-17)
        # Vertical line at x=0, spanning from inner wall (y=-12) to outer wall (y=-20)
        self.checkpoint1 = (np.array([0, -20]), np.array([0, -12]))  # Vertical line at bottom
        # Checkpoint 2: Halfway checkpoint at top
        # Vertical line at x=0, spanning from inner wall (y=12) to outer wall (y=20)
        self.checkpoint2 = (np.array([0, 12]), np.array([0, 20]))  # Vertical line at top

        # Track checkpoint states
        self.checkpoint1_crossed = False
        self.checkpoint2_crossed = False

        print(f"Checkpoint 1 (finish): {self.checkpoint1[0]} to {self.checkpoint1[1]}")
        print(f"Checkpoint 2 (halfway): {self.checkpoint2[0]} to {self.checkpoint2[1]}")

    def _create_oval_track(self):
        """Create an oval track"""
        # Outer boundary
        outer_points = []
        inner_points = []

        num_points = 60
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * math.pi

            # Oval shape (wider than tall)
            x = 30 * math.cos(angle)
            y = 20 * math.sin(angle)
            outer_points.append(np.array([x, y]))

            # Inner boundary (smaller oval)
            x_inner = 20 * math.cos(angle)
            y_inner = 12 * math.sin(angle)
            inner_points.append(np.array([x_inner, y_inner]))

        # Create wall segments
        for i in range(len(outer_points) - 1):
            self.walls.append((outer_points[i], outer_points[i + 1]))
            self.walls.append((inner_points[i], inner_points[i + 1]))

    def check_collision(self, pos, radius=1.0):
        """Check if position collides with track walls"""
        for wall in self.walls:
            if self._point_to_segment_distance(pos, wall) < radius:
                return True
        return False

    def _point_to_segment_distance(self, point, segment):
        """Calculate distance from point to line segment"""
        p1, p2 = segment
        line_vec = p2 - p1
        point_vec = point - p1
        line_len = np.linalg.norm(line_vec)

        if line_len < 1e-6:
            return np.linalg.norm(point_vec)

        line_unitvec = line_vec / line_len
        proj_length = np.dot(point_vec, line_unitvec)
        proj_length = max(0, min(line_len, proj_length))

        nearest = p1 + line_unitvec * proj_length
        return np.linalg.norm(point - nearest)

    def check_checkpoints(self, old_pos, new_pos):
        """Check if car crossed checkpoints and return lap completion status"""
        if old_pos is None or new_pos is None:
            return False

        # Check checkpoint 2 (halfway point at top) - must be crossed first
        if not self.checkpoint2_crossed:
            p1, p2 = self.checkpoint2
            if self._segments_intersect(old_pos, new_pos, p1, p2):
                self.checkpoint2_crossed = True
                print(f"✓ Checkpoint 2 (halfway) crossed! Position: {new_pos}")

        # Check checkpoint 1 (finish line at bottom) - only counts if checkpoint 2 was crossed
        elif not self.checkpoint1_crossed:
            p1, p2 = self.checkpoint1
            if self._segments_intersect(old_pos, new_pos, p1, p2):
                self.checkpoint1_crossed = True
                print(f"✓ Checkpoint 1 (finish) crossed! Position: {new_pos}")
                return True  # Lap complete!

        return False

    def _segments_intersect(self, a1, a2, b1, b2):
        """Check if two line segments intersect"""
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        return ccw(a1, b1, b2) != ccw(a2, b1, b2) and ccw(a1, a2, b1) != ccw(a1, a2, b2)

    def render(self):
        """Render track in 3D"""
        # Draw track surface (darker gray)
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        for i in range(0, len(self.walls) // 2 - 1):
            # Get outer and inner wall segments
            outer1, outer2 = self.walls[i * 2]
            inner1, inner2 = self.walls[i * 2 + 1]

            # Draw track surface quad
            glVertex3f(outer1[0], 0.05, outer1[1])
            glVertex3f(outer2[0], 0.05, outer2[1])
            glVertex3f(inner2[0], 0.05, inner2[1])
            glVertex3f(inner1[0], 0.05, inner1[1])
        glEnd()

        # Draw solid walls
        glColor3f(0.5, 0.5, 0.5)
        for wall in self.walls:
            p1, p2 = wall
            # Draw solid wall faces
            glBegin(GL_QUADS)
            # Front face
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            glVertex3f(p2[0], 2, p2[1])
            glVertex3f(p1[0], 2, p1[1])
            glEnd()

        # Draw wall outlines for definition
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINES)
        for wall in self.walls:
            p1, p2 = wall
            # Bottom edge
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            # Top edge
            glVertex3f(p1[0], 2, p1[1])
            glVertex3f(p2[0], 2, p2[1])
            # Vertical edges
            glVertex3f(p1[0], 0, p1[1])
            glVertex3f(p1[0], 2, p1[1])
            glVertex3f(p2[0], 0, p2[1])
            glVertex3f(p2[0], 2, p2[1])
        glEnd()

        # Draw checkpoint lines
        # Checkpoint 1 (finish line at bottom) - checkered pattern
        p1, p2 = self.checkpoint1
        num_squares = 8
        square_width = np.linalg.norm(p2 - p1) / num_squares
        direction = (p2 - p1) / np.linalg.norm(p2 - p1)
        perpendicular = np.array([-direction[1], direction[0]])  # 90 degree rotation

        for i in range(num_squares):
            if i % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)  # White
            else:
                glColor3f(0.0, 0.0, 0.0)  # Black

            start = p1 + direction * (i * square_width)
            end = p1 + direction * ((i + 1) * square_width)

            glBegin(GL_QUADS)
            glVertex3f(start[0] - perpendicular[0] * 0.5, 0.15, start[1] - perpendicular[1] * 0.5)
            glVertex3f(end[0] - perpendicular[0] * 0.5, 0.15, end[1] - perpendicular[1] * 0.5)
            glVertex3f(end[0] + perpendicular[0] * 0.5, 0.15, end[1] + perpendicular[1] * 0.5)
            glVertex3f(start[0] + perpendicular[0] * 0.5, 0.15, start[1] + perpendicular[1] * 0.5)
            glEnd()

        # Checkpoint 2 (halfway at top) - blue/green line
        p1, p2 = self.checkpoint2
        if self.checkpoint2_crossed:
            glColor3f(0.0, 1.0, 0.0)  # Green when crossed
        else:
            glColor3f(0.0, 0.5, 1.0)  # Blue when not crossed

        direction = (p2 - p1) / np.linalg.norm(p2 - p1)
        perpendicular = np.array([-direction[1], direction[0]])

        glBegin(GL_QUADS)
        glVertex3f(p1[0] - perpendicular[0] * 0.5, 0.15, p1[1] - perpendicular[1] * 0.5)
        glVertex3f(p2[0] - perpendicular[0] * 0.5, 0.15, p2[1] - perpendicular[1] * 0.5)
        glVertex3f(p2[0] + perpendicular[0] * 0.5, 0.15, p2[1] + perpendicular[1] * 0.5)
        glVertex3f(p1[0] + perpendicular[0] * 0.5, 0.15, p1[1] + perpendicular[1] * 0.5)
        glEnd()


class Car:
    """Car with physics simulation"""

    def __init__(self, x=0, y=-17.0):  # Start further back, outside the track
        self.pos = np.array([x, y], dtype=float)
        self.velocity = np.array([0.0, 0.0])
        self.angle = 0.0  # degrees, 0 is right (into the track), 90 is up
        self.wheel_angle = 0.0  # steering angle

        self.acceleration = 0.0
        self.max_speed = 150.0  # Higher max speed for faster racing
        self.friction = 0.98  # Lower friction for better speed (higher value = less friction)
        self.turn_speed = 12.0  # Responsive steering

        # Hitbox dimensions (width and length)
        self.width = 2.4  # Car width
        self.length = 5.0  # Car length (including nose)
        self.crashed = False

        print(f"Car initialized at position: {self.pos}, angle: {self.angle}")

    def get_corners(self):
        """Get the four corners of the car's hitbox"""
        angle_rad = math.radians(self.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)

        # Half dimensions
        hw = self.width / 2
        hl = self.length / 2

        # Local corners (relative to car center)
        corners_local = [
            (-hw, -hl),  # Back left
            (hw, -hl),   # Back right
            (hw, hl),    # Front right
            (-hw, hl),   # Front left
        ]

        # Rotate and translate to world space
        corners_world = []
        for lx, ly in corners_local:
            wx = self.pos[0] + lx * cos_a - ly * sin_a
            wy = self.pos[1] + lx * sin_a + ly * cos_a
            corners_world.append(np.array([wx, wy]))

        return corners_world

    def update(self, dt, track):
        """Update car physics"""
        # Apply acceleration
        angle_rad = math.radians(self.angle)
        accel_vec = np.array([
            math.cos(angle_rad) * self.acceleration,
            math.sin(angle_rad) * self.acceleration
        ])

        self.velocity += accel_vec * dt

        # Apply friction
        self.velocity *= self.friction

        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

        # Apply steering (only when moving)
        # Steering effectiveness increases with speed, but has minimum to prevent getting stuck
        if speed > 0.5:
            # Use a minimum factor of 0.2 to ensure steering works even at low speeds
            speed_factor = max(0.2, speed / self.max_speed)
            turn_amount = self.wheel_angle * self.turn_speed * dt * speed_factor
            self.angle += turn_amount

            # Align velocity more with car direction to reduce sliding
            # This gives the car better grip by pulling velocity toward the car's facing direction
            # Use lighter grip to avoid slowing down the car
            current_vel_angle = math.atan2(self.velocity[1], self.velocity[0])
            car_angle_rad = math.radians(self.angle)
            angle_diff = car_angle_rad - current_vel_angle

            # Normalize angle difference to [-pi, pi]
            while angle_diff > math.pi:
                angle_diff -= 2 * math.pi
            while angle_diff < -math.pi:
                angle_diff += 2 * math.pi

            # Apply grip: pull velocity toward car direction to reduce sliding
            # Use stronger grip at higher speeds for better control
            grip_strength = min(0.4, 0.2 + speed / self.max_speed * 0.4)  # 0.2 to 0.4 based on speed
            vel_angle_correction = angle_diff * grip_strength
            new_vel_angle = current_vel_angle + vel_angle_correction

            # Update velocity direction while maintaining speed (this doesn't reduce speed, just aligns direction)
            self.velocity = np.array([
                math.cos(new_vel_angle) * speed,
                math.sin(new_vel_angle) * speed
            ])

        # Update position
        old_pos = self.pos.copy()
        self.pos += self.velocity * dt

        # Check collision - use car center with radius based on car dimensions
        # Calculate half-diagonal for collision radius
        half_diagonal = math.sqrt((self.width/2)**2 + (self.length/2)**2)
        # Use a slightly smaller radius to avoid false positives, but account for car size
        collision_radius = half_diagonal * 0.9

        collision = track.check_collision(self.pos, collision_radius)

        if collision:
            self.pos = old_pos
            self.velocity *= -0.3  # Bounce back with reduced speed
            self.crashed = True
            print(f"Hit wall at position {self.pos}, speed: {np.linalg.norm(self.velocity):.2f}")
        else:
            self.crashed = False  # Reset crash state when clear

        return old_pos

    def render(self):
        """Render car in 3D - looks like a race car"""
        glPushMatrix()
        glTranslatef(self.pos[0], 0.5, self.pos[1])
        glRotatef(-self.angle + 90, 0, 1, 0)

        # Main body color
        if self.crashed:
            body_color = (1.0, 0.2, 0.2)  # Light red when crashed
        else:
            body_color = (0.2, 0.4, 1.0)  # Blue

        # Main car body (lower part)
        glColor3f(*body_color)
        glBegin(GL_QUADS)
        # Bottom
        glVertex3f(-1.2, 0, -2.0)
        glVertex3f(1.2, 0, -2.0)
        glVertex3f(1.2, 0, 2.0)
        glVertex3f(-1.2, 0, 2.0)
        # Top
        glVertex3f(-1.2, 0.8, -2.0)
        glVertex3f(1.2, 0.8, -2.0)
        glVertex3f(1.2, 0.8, 2.0)
        glVertex3f(-1.2, 0.8, 2.0)
        # Front
        glVertex3f(-1.2, 0, 2.0)
        glVertex3f(1.2, 0, 2.0)
        glVertex3f(1.2, 0.8, 2.0)
        glVertex3f(-1.2, 0.8, 2.0)
        # Back
        glVertex3f(-1.2, 0, -2.0)
        glVertex3f(1.2, 0, -2.0)
        glVertex3f(1.2, 0.8, -2.0)
        glVertex3f(-1.2, 0.8, -2.0)
        # Left side
        glVertex3f(-1.2, 0, -2.0)
        glVertex3f(-1.2, 0.8, -2.0)
        glVertex3f(-1.2, 0.8, 2.0)
        glVertex3f(-1.2, 0, 2.0)
        # Right side
        glVertex3f(1.2, 0, -2.0)
        glVertex3f(1.2, 0.8, -2.0)
        glVertex3f(1.2, 0.8, 2.0)
        glVertex3f(1.2, 0, 2.0)
        glEnd()

        # Cockpit/cabin (raised section)
        glColor3f(0.1, 0.1, 0.1)  # Dark gray/black
        glBegin(GL_QUADS)
        # Top
        glVertex3f(-0.8, 1.3, -0.5)
        glVertex3f(0.8, 1.3, -0.5)
        glVertex3f(0.8, 1.3, 1.0)
        glVertex3f(-0.8, 1.3, 1.0)
        # Front
        glVertex3f(-0.8, 0.8, 1.0)
        glVertex3f(0.8, 0.8, 1.0)
        glVertex3f(0.8, 1.3, 1.0)
        glVertex3f(-0.8, 1.3, 1.0)
        # Back
        glVertex3f(-0.8, 0.8, -0.5)
        glVertex3f(0.8, 0.8, -0.5)
        glVertex3f(0.8, 1.3, -0.5)
        glVertex3f(-0.8, 1.3, -0.5)
        # Sides
        glVertex3f(-0.8, 0.8, -0.5)
        glVertex3f(-0.8, 1.3, -0.5)
        glVertex3f(-0.8, 1.3, 1.0)
        glVertex3f(-0.8, 0.8, 1.0)
        glVertex3f(0.8, 0.8, -0.5)
        glVertex3f(0.8, 1.3, -0.5)
        glVertex3f(0.8, 1.3, 1.0)
        glVertex3f(0.8, 0.8, 1.0)
        glEnd()

        # Front nose (pointed)
        glColor3f(1.0, 0.8, 0.0)  # Yellow/gold
        glBegin(GL_TRIANGLES)
        # Top triangle
        glVertex3f(0, 0.8, 3.0)
        glVertex3f(-1.2, 0.8, 2.0)
        glVertex3f(1.2, 0.8, 2.0)
        # Bottom triangle
        glVertex3f(0, 0, 3.0)
        glVertex3f(-1.2, 0, 2.0)
        glVertex3f(1.2, 0, 2.0)
        # Left side
        glVertex3f(0, 0.8, 3.0)
        glVertex3f(-1.2, 0.8, 2.0)
        glVertex3f(0, 0, 3.0)
        glVertex3f(-1.2, 0.8, 2.0)
        glVertex3f(-1.2, 0, 2.0)
        glVertex3f(0, 0, 3.0)
        # Right side
        glVertex3f(0, 0.8, 3.0)
        glVertex3f(1.2, 0.8, 2.0)
        glVertex3f(0, 0, 3.0)
        glVertex3f(1.2, 0.8, 2.0)
        glVertex3f(1.2, 0, 2.0)
        glVertex3f(0, 0, 3.0)
        glEnd()

        # Rear wing
        glColor3f(0.8, 0.8, 0.8)  # Light gray
        glBegin(GL_QUADS)
        glVertex3f(-1.5, 1.2, -2.0)
        glVertex3f(1.5, 1.2, -2.0)
        glVertex3f(1.5, 1.2, -2.3)
        glVertex3f(-1.5, 1.2, -2.3)
        glEnd()

        # Wheels (simple cylinders as boxes)
        glColor3f(0.1, 0.1, 0.1)  # Black
        wheel_positions = [
            (-1.0, -0.3, 1.5),   # Front left
            (1.0, -0.3, 1.5),    # Front right
            (-1.0, -0.3, -1.5),  # Back left
            (1.0, -0.3, -1.5),   # Back right
        ]
        for wx, wy, wz in wheel_positions:
            glBegin(GL_QUADS)
            # Simple wheel representation
            glVertex3f(wx - 0.3, wy, wz - 0.4)
            glVertex3f(wx + 0.3, wy, wz - 0.4)
            glVertex3f(wx + 0.3, wy + 0.6, wz - 0.4)
            glVertex3f(wx - 0.3, wy + 0.6, wz - 0.4)
            glVertex3f(wx - 0.3, wy, wz + 0.4)
            glVertex3f(wx + 0.3, wy, wz + 0.4)
            glVertex3f(wx + 0.3, wy + 0.6, wz + 0.4)
            glVertex3f(wx - 0.3, wy + 0.6, wz + 0.4)
            glEnd()

        glPopMatrix()


class RaceGame:
    """Main game class"""

    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 800
        self.screen = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Race Timmy - Drive the lap!")

        # Setup OpenGL
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.5, 0.7, 1.0, 1.0)  # Sky blue background
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, (self.width / self.height), 0.1, 500.0)
        glMatrixMode(GL_MODELVIEW)

        # Game objects
        self.track = Track()
        self.car = Car()
        self.lidar = LidarSensor()
        self.controller = CarController()

        # Game state
        self.running = True
        self.paused = False
        self.lap_completed = False
        self.clock = pygame.time.Clock()

        # Timer (tracks elapsed time, pauses when paused)
        self.elapsed_time = 0.0
        self.last_update_time = time.time()

        self.lap_time = None
        self.lap_count = 0

        # Camera control
        self.camera_distance = 40
        self.camera_angle = 0
        self.camera_height = 25
        self.mouse_dragging = False
        self.last_mouse_pos = None

        # Font for UI (not used anymore but keep for compatibility)
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_SPACE:
                    self.paused = not self.paused
                elif event.key == K_r:
                    self.reset()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click - start camera drag
                    self.mouse_dragging = True
                    self.last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:  # Scroll up
                    self.camera_distance = max(10, self.camera_distance - 2)
                elif event.button == 5:  # Scroll down
                    self.camera_distance = min(100, self.camera_distance + 2)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_dragging = False
            elif event.type == MOUSEMOTION:
                if self.mouse_dragging and self.last_mouse_pos:
                    dx = event.pos[0] - self.last_mouse_pos[0]
                    dy = event.pos[1] - self.last_mouse_pos[1]
                    self.camera_angle += dx * 0.5
                    self.camera_height = max(5, min(50, self.camera_height - dy * 0.2))
                    self.last_mouse_pos = event.pos

    def reset(self):
        """Reset the race"""
        self.car = Car()
        # Reset track checkpoint states
        self.track.checkpoint1_crossed = False
        self.track.checkpoint2_crossed = False
        self.elapsed_time = 0.0
        self.last_update_time = time.time()
        self.lap_time = None
        self.lap_count = 0
        self.lap_completed = False
        self.paused = False

    def update(self, dt):
        """Update game state"""
        # Update timer (only when not paused and lap not completed)
        current_time = time.time()
        if not self.paused and not self.lap_completed:
            self.elapsed_time += current_time - self.last_update_time
        self.last_update_time = current_time

        # Don't update physics if paused or lap completed
        if self.paused or self.lap_completed:
            return

        # Get LIDAR data
        lidar_data = self.lidar.scan(self.car.pos, self.car.angle, self.track)

        # Call student's controller
        try:
            result = self.controller.control(lidar_data)
            if result is None:
                print("WARNING: controller.control() returned None!")
                acceleration, wheel_angle = 0, 0
            else:
                acceleration, wheel_angle = result
                # Debug output every 60 frames (once per second at 60fps)
                if int(time.time() * 60) % 60 == 0:
                    print(f"Controller: accel={acceleration:.1f}, wheel={wheel_angle:.1f}, speed={np.linalg.norm(self.car.velocity):.1f}")
        except Exception as e:
            print(f"Error in controller: {e}")
            import traceback
            traceback.print_exc()
            acceleration, wheel_angle = 0, 0

        # Clamp values - allow higher acceleration for speed
        self.car.acceleration = max(-20, min(20, acceleration))  # Increased from 10 to 20
        self.car.wheel_angle = max(-45, min(45, wheel_angle))

        # Update car
        old_pos = self.car.update(dt, self.track)

        # Check lap completion
        if old_pos is not None:
            # Debug: print car position every 2 seconds
            if int(self.elapsed_time * 0.5) % 2 == 0 and int(self.elapsed_time * 10) % 10 == 0:
                print(f"Car position: {self.car.pos}, Lap count: {self.lap_count}")

            lap_complete = self.track.check_checkpoints(old_pos, self.car.pos)
            if lap_complete:
                self.lap_time = self.elapsed_time
                self.lap_completed = True
                print(f"\n{'='*50}")
                print(f"🏁 LAP COMPLETED! 🏁")
                print(f"Time: {self.lap_time:.2f} seconds")
                print(f"{'='*50}\n")

    def render(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera follows car with mouse control
        angle_rad = math.radians(self.camera_angle)
        cam_x = self.car.pos[0] + self.camera_distance * math.sin(angle_rad)
        cam_z = self.car.pos[1] + self.camera_distance * math.cos(angle_rad)

        gluLookAt(
            cam_x, self.camera_height, cam_z,
            self.car.pos[0], 0, self.car.pos[1],
            0, 1, 0
        )

        # Draw ground (grass)
        glColor3f(0.2, 0.6, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-100, 0, -100)
        glVertex3f(100, 0, -100)
        glVertex3f(100, 0, 100)
        glVertex3f(-100, 0, 100)
        glEnd()

        # Draw track and car
        self.track.render()
        self.car.render()

        # Draw LIDAR visualization
        self._render_lidar()

        # Draw 2D UI overlay (before flip!)
        self._render_ui()

        pygame.display.flip()

    def _render_lidar(self):
        """Visualize LIDAR rays"""
        lidar_data = self.lidar.scan(self.car.pos, self.car.angle, self.track)

        glColor3f(0.0, 1.0, 0.0)
        glBegin(GL_LINES)
        for i, distance in enumerate(lidar_data):
            angle_offset = self.lidar.angles[i]
            ray_angle = math.radians(self.car.angle + angle_offset)

            end_x = self.car.pos[0] + distance * math.cos(ray_angle)
            end_y = self.car.pos[1] + distance * math.sin(ray_angle)

            glVertex3f(self.car.pos[0], 0.5, self.car.pos[1])
            glVertex3f(end_x, 0.5, end_y)
        glEnd()

    def _render_ui(self):
        """Render 2D UI overlay on top of 3D scene"""
        # Switch to 2D orthographic projection for UI
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, self.width, self.height, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Disable depth test for UI
        glDisable(GL_DEPTH_TEST)

        # Draw semi-transparent background for UI panel
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.0, 0.0, 0.0, 0.5)
        glBegin(GL_QUADS)
        glVertex2f(10, 10)
        glVertex2f(400, 10)
        glVertex2f(400, 120)
        glVertex2f(10, 120)
        glEnd()

        # Render text using pygame surface
        texts = []
        if self.lap_completed and self.lap_time:
            texts.append((f"LAP COMPLETE!", (0, 255, 0), 40))
            texts.append((f"Time: {self.lap_time:.2f}s", (255, 255, 255), 70))
            texts.append((f"Press R to restart", (200, 200, 200), 100))
        elif self.paused:
            texts.append((f"PAUSED", (255, 255, 0), 40))
            texts.append((f"Time: {self.elapsed_time:.2f}s", (255, 255, 255), 70))
            texts.append((f"Press SPACE to continue", (200, 200, 200), 100))
        else:
            texts.append((f"Time: {self.elapsed_time:.2f}s", (255, 255, 255), 40))
            texts.append((f"Speed: {np.linalg.norm(self.car.velocity):.1f}", (255, 255, 255), 70))
            texts.append((f"SPACE: Pause | R: Restart", (200, 200, 200), 100))

        for text, color, y_pos in texts:
            self._render_text(text, 20, y_pos, color)

        glDisable(GL_BLEND)

        # Re-enable depth test
        glEnable(GL_DEPTH_TEST)

        # Restore projection
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

        # Also update window title
        if self.lap_completed and self.lap_time:
            title = f"Race Timmy - LAP COMPLETE! Time: {self.lap_time:.2f}s"
        elif self.paused:
            title = f"Race Timmy - PAUSED"
        else:
            title = f"Race Timmy - Racing..."
        pygame.display.set_caption(title)

    def _render_text(self, text, x, y, color=(255, 255, 255)):
        """Render text on screen using pygame"""
        text_surface = self.font.render(text, True, color)
        text_data = pygame.image.tostring(text_surface, "RGBA", True)

        glRasterPos2f(x, y)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(),
                     GL_RGBA, GL_UNSIGNED_BYTE, text_data)

    def run(self):
        """Main game loop with fixed timestep physics"""
        # Fixed timestep for physics (60 FPS = 1/60 seconds per frame)
        FIXED_DT = 1.0 / 60.0

        while self.running:
            # Cap frame rate at 60 FPS
            self.clock.tick(60)

            self.handle_events()

            # Always update with fixed timestep
            self.update(FIXED_DT)

            # Render
            self.render()

        pygame.quit()


if __name__ == "__main__":
    game = RaceGame()
    game.run()
