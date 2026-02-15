<script lang="ts">
  import { onMount } from 'svelte';
  import { API_BASE_URL } from '$lib/api';

  interface Blog {
    id: number;
    title: string;
    slug: string;
    excerpt?: string;
    status: string;
    created_at: string;
    author?: string;
  }

  let blogs: Blog[] = [];
  let isLoading = true;
  let showCreateModal = false;
  let editingBlog: Blog | null = null;

  // Form fields
  let title = '';
  let content = '';
  let excerpt = '';
  let status = 'draft';
  let metaTitle = '';
  let metaDescription = '';
  let isSaving = false;
  let saveError = '';

  onMount(async () => {
    await fetchBlogs();
  });

  async function fetchBlogs() {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/blogs`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        blogs = await res.json();
      }
    } catch (e) {
      console.error('Failed to fetch blogs:', e);
    } finally {
      isLoading = false;
    }
  }

  function openCreateModal() {
    resetForm();
    showCreateModal = true;
  }

  function openEditModal(blog: Blog) {
    editingBlog = blog;
    title = blog.title;
    // Fetch full blog details
    fetchBlogDetails(blog.id);
    showCreateModal = true;
  }

  async function fetchBlogDetails(id: number) {
    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/blogs/${id}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        const blog = await res.json();
        title = blog.title;
        content = blog.content;
        excerpt = blog.excerpt || '';
        status = blog.status;
        metaTitle = blog.meta_title || '';
        metaDescription = blog.meta_description || '';
      }
    } catch (e) {
      console.error('Failed to fetch blog details:', e);
    }
  }

  function resetForm() {
    editingBlog = null;
    title = '';
    content = '';
    excerpt = '';
    status = 'draft';
    metaTitle = '';
    metaDescription = '';
    saveError = '';
  }

  function closeModal() {
    showCreateModal = false;
    resetForm();
  }

  async function saveBlog() {
    if (!title || !content) {
      saveError = 'Title and content are required';
      return;
    }

    isSaving = true;
    saveError = '';

    try {
      const token = localStorage.getItem('admin_token');
      const url = editingBlog
        ? `${API_BASE_URL}/admin/blogs/${editingBlog.id}`
        : `${API_BASE_URL}/admin/blogs`;
      
      const method = editingBlog ? 'PUT' : 'POST';

      const res = await fetch(url, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          title,
          content,
          excerpt,
          status,
          meta_title: metaTitle,
          meta_description: metaDescription
        })
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || 'Failed to save blog');
      }

      await fetchBlogs();
      closeModal();
    } catch (e: any) {
      saveError = e.message;
    } finally {
      isSaving = false;
    }
  }

  async function deleteBlog(id: number) {
    if (!confirm('Are you sure you want to delete this blog?')) return;

    try {
      const token = localStorage.getItem('admin_token');
      const res = await fetch(`${API_BASE_URL}/admin/blogs/${id}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (res.ok) {
        await fetchBlogs();
      }
    } catch (e) {
      console.error('Failed to delete blog:', e);
    }
  }

  function formatDate(dateStr: string) {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }
</script>

<div class="p-8">
  <!-- Header -->
  <div class="flex items-center justify-between mb-8">
    <div>
      <h1 class="text-3xl font-bold text-slate-800 mb-2">Blog Management</h1>
      <p class="text-slate-600">Create and manage blog posts</p>
    </div>
    <button
      on:click={openCreateModal}
      class="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition flex items-center gap-2"
    >
      <span class="text-xl">+</span>
      Create Blog
    </button>
  </div>

  {#if isLoading}
    <div class="flex items-center justify-center py-20">
      <svg class="animate-spin h-8 w-8 text-red-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
  {:else if blogs.length === 0}
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 p-12 text-center">
      <div class="text-6xl mb-4">📝</div>
      <h3 class="text-xl font-semibold text-slate-800 mb-2">No blogs yet</h3>
      <p class="text-slate-600 mb-6">Create your first blog post to get started</p>
      <button
        on:click={openCreateModal}
        class="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition"
      >
        Create Blog
      </button>
    </div>
  {:else}
    <!-- Blogs Table -->
    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
      <table class="w-full">
        <thead class="bg-slate-50 border-b border-slate-200">
          <tr>
            <th class="px-6 py-4 text-left text-sm font-semibold text-slate-700">Title</th>
            <th class="px-6 py-4 text-left text-sm font-semibold text-slate-700">Status</th>
            <th class="px-6 py-4 text-left text-sm font-semibold text-slate-700">Author</th>
            <th class="px-6 py-4 text-left text-sm font-semibold text-slate-700">Created</th>
            <th class="px-6 py-4 text-right text-sm font-semibold text-slate-700">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-slate-200">
          {#each blogs as blog}
            <tr class="hover:bg-slate-50 transition">
              <td class="px-6 py-4">
                <div>
                  <p class="font-medium text-slate-800">{blog.title}</p>
                  {#if blog.excerpt}
                    <p class="text-sm text-slate-600 mt-1 line-clamp-1">{blog.excerpt}</p>
                  {/if}
                </div>
              </td>
              <td class="px-6 py-4">
                <span class="px-3 py-1 rounded-full text-xs font-medium {blog.status === 'published' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}">
                  {blog.status}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-slate-600">{blog.author || 'Unknown'}</td>
              <td class="px-6 py-4 text-sm text-slate-600">{formatDate(blog.created_at)}</td>
              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button
                    on:click={() => openEditModal(blog)}
                    class="px-3 py-1 text-sm text-blue-600 hover:bg-blue-50 rounded transition"
                  >
                    Edit
                  </button>
                  <button
                    on:click={() => deleteBlog(blog.id)}
                    class="px-3 py-1 text-sm text-red-600 hover:bg-red-50 rounded transition"
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<!-- Create/Edit Modal -->
{#if showCreateModal}
  <!-- svelte-ignore a11y-click-events-have-key-events -->
  <!-- svelte-ignore a11y-no-static-element-interactions -->
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" on:click={closeModal}>
    <div class="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] overflow-auto" on:click|stopPropagation role="dialog" aria-modal="true">
      <div class="sticky top-0 bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between">
        <h2 class="text-2xl font-bold text-slate-800">
          {editingBlog ? 'Edit Blog' : 'Create New Blog'}
        </h2>
        <button on:click={closeModal} class="text-slate-400 hover:text-slate-600 transition">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-6">
        <!-- Title -->
        <div>
          <label for="blog-title" class="block text-sm font-medium text-slate-700 mb-2">Title *</label>
          <input
            id="blog-title"
            type="text"
            bind:value={title}
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
            placeholder="Enter blog title"
          />
        </div>

        <!-- Content -->
        <div>
          <label for="blog-content" class="block text-sm font-medium text-slate-700 mb-2">Content *</label>
          <textarea
            id="blog-content"
            bind:value={content}
            rows="10"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none resize-none"
            placeholder="Write your blog content here (supports Markdown)"
          ></textarea>
        </div>

        <!-- Excerpt -->
        <div>
          <label for="blog-excerpt" class="block text-sm font-medium text-slate-700 mb-2">Excerpt</label>
          <textarea
            id="blog-excerpt"
            bind:value={excerpt}
            rows="3"
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none resize-none"
            placeholder="Short description (optional)"
          ></textarea>
        </div>

        <!-- Status -->
        <div>
          <label for="blog-status" class="block text-sm font-medium text-slate-700 mb-2">Status</label>
          <select
            id="blog-status"
            bind:value={status}
            class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
          >
            <option value="draft">Draft</option>
            <option value="published">Published</option>
          </select>
        </div>

        <!-- SEO Section -->
        <div class="border-t border-slate-200 pt-6">
          <h3 class="text-lg font-semibold text-slate-800 mb-4">SEO Settings</h3>
          
          <div class="space-y-4">
            <div>
              <label for="blog-meta-title" class="block text-sm font-medium text-slate-700 mb-2">Meta Title</label>
              <input
                id="blog-meta-title"
                type="text"
                bind:value={metaTitle}
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none"
                placeholder="SEO title (optional, defaults to blog title)"
              />
            </div>

            <div>
              <label for="blog-meta-desc" class="block text-sm font-medium text-slate-700 mb-2">Meta Description</label>
              <textarea
                id="blog-meta-desc"
                bind:value={metaDescription}
                rows="2"
                class="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-transparent outline-none resize-none"
                placeholder="SEO description (optional, defaults to excerpt)"
              ></textarea>
            </div>
          </div>
        </div>

        {#if saveError}
          <div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            ⚠️ {saveError}
          </div>
        {/if}

        <!-- Actions -->
        <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-200">
          <button
            on:click={closeModal}
            class="px-6 py-2 border border-slate-300 text-slate-700 hover:bg-slate-50 rounded-lg transition"
          >
            Cancel
          </button>
          <button
            on:click={saveBlog}
            disabled={isSaving}
            class="px-6 py-2 bg-red-600 hover:bg-red-700 text-white font-semibold rounded-lg transition disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2"
          >
            {#if isSaving}
              <svg class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Saving...
            {:else}
              {editingBlog ? 'Update' : 'Create'} Blog
            {/if}
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}
