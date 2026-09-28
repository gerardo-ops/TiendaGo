-- =========================================================================
-- TIENDAGO: Script de Sembrado para Usuario Administrador por Defecto
-- Compatible con Supabase Auth (auth.users) y tabla pública de Usuarios (public.usuarios)
-- =========================================================================

-- 1. Habilitar extensión pgcrypto para hashing de contraseñas con BCrypt
CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
DECLARE
    v_user_id uuid := '37907a7d-4609-422f-b02b-6799bb01c8f2';
    v_email text := 'admin@tiendago.com';
    v_password text := 'Admin123*';
    v_full_name text := 'Administrador TiendaGo';
    v_role_id bigint := 1;
    v_hash text;
BEGIN
    -- 2. Asegurar que los roles base existan
    INSERT INTO public.roles (id_rol, nombre_rol, descripcion)
    VALUES 
        (1, 'Administrador', 'Control total de inventario, catálogo, reportes y configuración de usuarios'),
        (2, 'Cajero', 'Operación de terminal POS de ventas, apertura y cierre de turnos de caja'),
        (3, 'Supervisor', 'Auditoría de historial de ventas, métricas de rendimiento y cuadre de cajas')
    ON CONFLICT (id_rol) DO NOTHING;

    -- 3. Generar hash BCrypt compatible con BCrypt.Net y Supabase Auth
    v_hash := crypt(v_password, gen_salt('bf', 6));

    -- 4. Insertar o actualizar en auth.users (para cumplir con FK usuarios_id_usuario_fkey)
    IF EXISTS (SELECT 1 FROM auth.users WHERE email = v_email) THEN
        UPDATE auth.users 
        SET encrypted_password = v_hash,
            updated_at = now()
        WHERE email = v_email
        RETURNING id INTO v_user_id;
    ELSE
        INSERT INTO auth.users (
            instance_id,
            id,
            aud,
            role,
            email,
            encrypted_password,
            email_confirmed_at,
            created_at,
            updated_at,
            raw_app_meta_data,
            raw_user_meta_data,
            is_super_admin
        ) VALUES (
            '00000000-0000-0000-0000-000000000000',
            v_user_id,
            'authenticated',
            'authenticated',
            v_email,
            v_hash,
            now(),
            now(),
            now(),
            '{"provider":"email","providers":["email"]}'::jsonb,
            jsonb_build_object('full_name', v_full_name),
            false
        );
    END IF;

    -- 5. Insertar o actualizar en public.usuarios
    INSERT INTO public.usuarios (
        id_usuario,
        id_rol,
        nombre_completo,
        correo_electronico,
        clave_hash,
        estado_activo,
        fecha_registro
    ) VALUES (
        v_user_id,
        v_role_id,
        v_full_name,
        v_email,
        v_hash,
        true,
        now()
    )
    ON CONFLICT (correo_electronico) DO UPDATE SET
        id_usuario = EXCLUDED.id_usuario,
        id_rol = EXCLUDED.id_rol,
        nombre_completo = EXCLUDED.nombre_completo,
        clave_hash = EXCLUDED.clave_hash,
        estado_activo = true;

    RAISE NOTICE 'Usuario Administrador insertado/actualizado correctamente: % (ID: %)', v_email, v_user_id;
END $$;
